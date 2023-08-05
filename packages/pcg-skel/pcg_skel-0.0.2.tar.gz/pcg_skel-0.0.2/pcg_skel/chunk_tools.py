import numpy as np
from scipy import spatial
import cloudvolume
from . import utils, chunk_cache
import multiwrapper.multiprocessing_utils as mu

UnshardedMeshSource = cloudvolume.datasource.graphene.mesh.unsharded.GrapheneUnshardedMeshSource
ShardedMeshSource = cloudvolume.datasource.graphene.mesh.sharded.GrapheneShardedMeshSource


def refine_vertices(
    vertices,
    l2dict_reversed,
    cv,
    refine_inds='all',
    scale_chunk_index=True,
    convert_missing=False,
    return_missing_ids=True,
    cache=None,
    save_to_cache=False,
    segmentation_fallback=True,
):
    """Refine vertices in chunk index space by converting to euclidean space using a combination of mesh downloading and simple chunk mapping.

    Parameters
    ----------
    vertices : array
        Nx3 array of vertex locations in chunk index space
    l2dict_reversed : dict or array
        N-length mapping from vertex index to uint64 level 2 id.
    cv : cloudvolume.CloudVolume
        CloudVolume associated with the chunkedgraph instance
    refine_inds : array, string, or None, optional
        Array of indices to refine via mesh download and recentering, None, or 'all'. If 'all', does all vertices. By default 'all'.
    scale_chunk_index : bool, optional
        If True, moves chunk indices to the euclidean space (the center of the chunk) if not refined. by default True.
    convert_missing : bool, optional
        If True, vertices with missing meshes are converted to the center of their chunk. Otherwise, they are given nans. By default, False.
    return_missing_ids : bool, optional
        If True, returns a list of level 2 ids for which meshes were not found, by default True
    segmentation_fallback : bool, optional
        If True, uses the segmentation as a fallback if the mesh does not exist.

    Returns
    -------
    new_vertices : array
        Nx3 array of remapped vertex locations in euclidean space
    missing_ids : array, optional
        List of level 2 ids without meshes. Only returned if return_missing_ids is True.
    """
    vertices = vertices.copy()
    if refine_inds == 'all':
        refine_inds = np.arange(0, len(vertices))

    if refine_inds is not None:
        l2ids = [l2dict_reversed[k] for k in refine_inds]
        pt_locs, missing_ids = lvl2_fragment_locs(
            l2ids, cv, return_missing=True, cache=cache, save_to_cache=save_to_cache,
            segmentation_fallback=segmentation_fallback)

        if convert_missing:
            missing_inds = np.any(np.isnan(pt_locs), axis=1)
            vertices[refine_inds[~missing_inds]] = pt_locs[~missing_inds]
        else:
            missing_inds = np.full(len(pt_locs), False)
            vertices[refine_inds] = pt_locs
    else:
        refine_inds = np.array([], dtype=int)
        missing_inds = np.array([], dtype=bool)
        missing_ids = np.array([], dtype=int)

    if scale_chunk_index and len(refine_inds) != len(vertices):
        # Move unrefined vertices to center of chunks
        other_inds = np.full(len(vertices), True)
        if len(refine_inds) > 0:
            other_inds[refine_inds[~missing_inds]] = False
        vertices[other_inds] = (
            utils.chunk_to_nm(vertices[other_inds], cv) +
            utils.chunk_dims(cv) // 2
        )
    if return_missing_ids:
        return vertices, missing_ids
    else:
        return vertices


def get_closest_lvl2_chunk(
    point,
    root_id,
    client,
    cv=None,
    voxel_resolution=[4, 4, 40],
    radius=200,
    return_point=False,
):
    """Get the closest level 2 chunk on a root id

    Parameters
    ----------
    point : array-like
        Point in voxel space.
    root_id : int
        Root id of the object
    client : FrameworkClient
        Framework client to access data
    cv : cloudvolume.CloudVolume or None, optional
        Cloudvolume associated with the dataset. One is created if None.
    voxel_resolution : list, optional
        Point resolution to map between point resolution and mesh resolution, by default [4, 4, 40]
    radius : int, optional
        Max distance to look for a nearby supervoxel. Optional, default is 200.
    return_point : bool, optional
        If True, returns the closest point in addition to the level 2 id. Optional, default is False.

    Returns
    -------
    level2_id : int
        Level 2 id of the object nearest to the point specified.
    close_point : array, optional
        Closest point inside the object to the specified point. Only returned if return_point is True.
    """
    if cv is None:
        cv = cloudvolume.CloudVolume(
            client.info.segmentation_source(),
            use_https=True,
            bounded=False,
            progress=False,
        )

    point = point * np.array(voxel_resolution)
    # Get the closest adjacent point for the root id within the radius.
    mip_scaling = np.array(cv.mip_resolution(0))

    pt = np.array(point) // mip_scaling
    offset = radius // mip_scaling
    lx = np.array(pt) - offset
    ux = np.array(pt) + offset
    bbox = cloudvolume.Bbox(lx, ux)
    vol = cv.download(bbox, segids=[root_id])
    vol = np.squeeze(vol)
    if not bool(np.any(vol > 0)):
        raise ValueError("No point of the root id is near the specified point")

    ctr = offset * point * voxel_resolution
    xyz = np.vstack(np.where(vol > 0)).T
    xyz_nm = xyz * mip_scaling * voxel_resolution

    ind = np.argmin(np.linalg.norm(xyz_nm - ctr, axis=1))
    closest_pt = vol.bounds.minpt + xyz[ind]

    # Look up the level 2 supervoxel for that id.
    closest_sv = int(cv.download_point(closest_pt, size=1))
    lvl2_id = client.chunkedgraph.get_root_id(closest_sv, level2=True)

    if return_point:
        return lvl2_id, closest_pt * mip_scaling * voxel_resolution
    else:
        return lvl2_id


def lvl2_fragment_locs(l2_ids, cv, return_missing=True, segmentation_fallback=True,
                       cache=None, save_to_cache=False):
    """ Look up representitive location for a list of level 2 ids.

    The representitive point for a mesh is the mesh vertex nearest to the
    centroid of the mesh fragment.

    Parameters
    ----------
    l2_ids : list-like
        List of N level 2 ids
    cv : cloudvolume.CloudVolume
        Associated cloudvolume object
    return_missing : bool, optional
        If True, returns ids of missing meshes. Default is True
    segmentation_fallback : bool, optional
        If True, uses segmentation to get the location if no mesh fragment is found.
        This is slower, but more robust. Default is True.
    cache: str or None, optional
        If a string, filename for a sqlite database used as a lookup cache for l2 ids.
        Default is None.
    save_to_cache: bool, optional
        If True and a chace is set, automatically saves looked up locations to the cache.
        Default is False.

    Returns
    -------
    l2means : np.array   
        Nx3 list of point locations. Missing mesh fragments get a nan for each component.
    missing_ids : np.array
        List of level 2 ids that were not found. Only returned if return_missing is True.
    """

    l2_ids = np.array(l2_ids)
    l2means = np.full((len(l2_ids), 3), np.nan, dtype=np.float)
    if cache is not None:
        l2means_cached, is_cached = chunk_cache.lookup_cached_ids(
            l2_ids, cache_file=cache)
    else:
        l2means_cached = np.zeros((0, 3), dtype=np.float)
        is_cached = np.full(len(l2_ids), False, dtype=np.bool)

    l2means[is_cached] = l2means_cached

    if np.any(~is_cached):
        l2means_dl, missing_ids = download_lvl2_locs(
            l2_ids[~is_cached], cv, segmentation_fallback)
        l2means[~is_cached] = l2means_dl
        if cache is not None and save_to_cache:
            chunk_cache.save_ids_to_cache(
                l2_ids[~is_cached], l2means_dl, cache)
    else:
        missing_ids = []

    if return_missing:
        return l2means, missing_ids
    else:
        return l2means


def download_lvl2_locs(l2_ids, cv, segmentation_fallback):
    if isinstance(cv.mesh, ShardedMeshSource):
        l2meshes = download_l2meshes(l2_ids, cv, sharded=True)
    else:
        l2meshes = download_l2meshes(l2_ids, cv, sharded=False)

    l2means = []
    args = []
    for l2id in l2_ids:
        args.append((l2id,
                     l2meshes.get(l2id, None),
                     f'graphene://{cv.meta.table_path}',
                     segmentation_fallback))

    print(f'Downloading {len(l2_ids)} locations with parallel={cv.parallel}')
    l2means = mu.multithread_func(
        _localize_l2_id_multi, args, n_threads=cv.parallel)

    if len(l2means) > 0:
        l2means = np.vstack(l2means)
        missing_ids = l2_ids[np.isnan(l2means[:, 0])]
    else:
        l2means = np.empty((0, 3), dtype=float)
        missing_ids = []
    return l2means, missing_ids


def _localize_l2_id_multi(args):
    l2id, l2mesh, cv_path, segmentation_fallback = args
    return _localize_l2_id(l2id, l2mesh, cv_path, segmentation_fallback)


def _localize_l2_id(l2id, l2mesh, cv_path, segmentation_fallback):
    if l2mesh is not None:
        l2m_abs = np.mean(l2mesh.vertices, axis=0)
        _, ii = spatial.cKDTree(l2mesh.vertices).query(l2m_abs)
        l2m = l2mesh.vertices[ii]
    else:
        if segmentation_fallback:
            cv = cloudvolume.CloudVolume(
                cv_path, bounded=False, progress=False, use_https=True, mip=0)
            l2m = chunk_location_from_segmentation(l2id, cv)
        else:
            l2m = np.array([np.nan, np.nan, np.nan])
    return l2m


def download_l2meshes(l2ids, cv, n_split=10, sharded=False):
    if cv.parallel > 1:
        splits = np.ceil(len(l2ids)/n_split)
        l2id_groups = np.array_split(l2ids, int(splits))
        args = []
        for l2id_group in l2id_groups:
            args.append((l2id_group, cv))

        progress = cv.progress
        cv.progress = False

        if sharded:
            meshes_indiv = mu.multithread_func(
                _download_l2meshes_sharded_multi, args, n_threads=cv.parallel)
        else:
            meshes_indiv = mu.multithread_func(
                _download_l2meshes_unsharded_multi, args, n_threads=cv.parallel)
        meshes_all_dict = {}
        for mdicts in meshes_indiv:
            meshes_all_dict.update(mdicts)

        cv.progress = progress
        return meshes_all_dict
    else:
        if sharded:
            return cv.mesh.get_meshes_on_bypass(l2ids, allow_missing=True)
        else:
            return cv.mesh.get(l2ids, allow_missing=True, deduplicate_chunk_boundaries=False)


def _download_l2meshes_unsharded_multi(args):
    root_id, cv = args
    return _download_l2meshes_unsharded(root_id, cv)


def _download_l2meshes_unsharded(mesh_ids, cv):
    try:
        ms = cv.mesh.get(
            mesh_ids, deduplicate_chunk_boundaries=False, allow_missing=True)
    except:
        ms = {}
    if len(ms) == 0:
        return {mesh_id: None for mesh_id in mesh_ids}
    else:
        return ms


def _download_l2meshes_sharded_multi(args):
    mesh_ids, cv = args
    return _download_l2meshes_sharded(mesh_ids, cv)


def _download_l2meshes_sharded(mesh_ids, cv):
    try:
        ms = cv.mesh.get_meshes_on_bypass(mesh_ids, allow_missing=True)
    except:
        ms = {}
    if len(ms) == 0:
        return {mesh_id: None for mesh_id in mesh_ids}
    else:
        return ms


def download_l2meshes_sharded(l2ids, cv):
    return cv.mesh.get_meshes_on_bypass(l2ids, allow_missing=True)


def chunk_location_from_segmentation(l2id, cv):
    """Representative level 2 id location using the segmentation.
    This is typically slower than the mesh approach, but is more robust.

    Parameters
    ----------
    l2id : int
        Level 2 id to look up
    cv : cloudvolume.CloudVolume
        CloudVolume associated with the mesh

    Returns
    -------
    xyz_rep : np.array
        3-element xyz array of the representative location in euclidean space.
    """
    loc_ch = np.array(cv.mesh.meta.meta.decode_chunk_position(l2id))
    loc_vox = np.atleast_2d(loc_ch) * cv.graph_chunk_size + \
        np.array(cv.voxel_offset)
    bbox = cloudvolume.Bbox(loc_vox[0], loc_vox[0] + cv.graph_chunk_size)

    sv_vol = cv.download(bbox, agglomerate=True, stop_layer=2,  mip=0)
    x, y, z = np.where(sv_vol.squeeze() == l2id)

    xyz = np.vstack((x, y, z)).T * np.array(sv_vol.resolution)

    xyz_mean = np.mean(xyz, axis=0)
    xyz_box = xyz[np.argmin(np.linalg.norm(xyz-xyz_mean, axis=1))]
    xyz_rep = np.array(sv_vol.bounds.minpt) * \
        np.array(sv_vol.resolution) + xyz_box
    return xyz_rep
