from typing import Any, Union, Literal

import numpy as np
from scipy.spatial import KDTree
from scipy.stats import binned_statistic_2d

def lon_to_180(lon: Any) -> Any:
    '''将经度换算到[-180, 180]范围内. 注意180会变成-180.'''
    return (lon + 180) % 360 - 180

def lon_to_360(lon: Any) -> Any:
    '''将经度换算到[0, 360]范围内.'''
    return lon % 360

def month_to_season(month: Any) -> Any:
    '''将月份换算为季节. 月份用[1, 12]表示, 季节用[1, 4]表示.'''
    return (month - 3) % 12 // 3 + 1

def polar_to_xy(r: Any, phi: Any, radians: bool = True) -> tuple[Any, Any]:
    '''极坐标转直角坐标.'''
    if not radians:
        phi = np.deg2rad(phi)
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    return x, y

def xy_to_polar(x: Any, y: Any, radians: bool = True) -> tuple[Any, Any]:
    '''直角坐标转极坐标. 角度范围[-pi, pi].'''
    r = np.hypot(x, y)
    phi = np.arctan2(y, x)
    if not radians:
        phi = np.rad2deg(phi)

    return r, phi

def wswd_to_uv(ws: Any, wd: Any) -> tuple[Any, Any]:
    '''风向风速转为uv.'''
    wd = np.deg2rad(wd)
    u = -ws * np.sin(wd)
    v = -ws * np.cos(wd)

    return u, v

def uv_to_wswd(u: Any, v: Any) -> tuple[Any, Any]:
    '''uv转为风向风速.'''
    ws = np.hypot(u, v)
    wd = np.rad2deg(np.arctan2(u, v)) + 180

    return ws, wd

def haversine(
    lon1: Any,
    lat1: Any,
    lon2: Any,
    lat2: Any,
    as_degrees: bool = False
) -> Any:
    '''利用haversine公式计算两点间的圆心角.'''
    lon1, lat1, lon2, lat2 = map(np.deg2rad, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    hav = lambda x: np.sin(x / 2)**2
    a = hav(dlat)
    b = np.cos(lat1) * np.cos(lat2) * hav(dlon)
    dtheta = 2 * np.arcsin(np.sqrt(a + b))
    if as_degrees:
        dtheta = np.rad2deg(dtheta)

    return dtheta

def region_ind(
    lon: Any,
    lat: Any,
    extents: Any,
    form: Literal['mask', 'ix'] = 'mask'
) -> Union[np.ndarray, tuple[np.ndarray, np.ndarray]]:
    '''
    返回落入给定经纬度方框范围内的索引.

    Parameters
    ----------
    lon : array_like
        经度. 若form='mask'则要求形状与lat一致.

    lat : array_like
        纬度. 若form='mask'则要求形状与lon一致.

    extents : (4,) array_like
        经纬度方框的范围[lonmin, lonmax, latmin, latmax].

    form : {'mask', 'ix'}
        索引的形式.
        'mask': 使用与lon和lat同形状的布尔数组进行索引.
        'ix': 使用下标构成的开放网格进行索引.

    Returns
    -------
    ind : ndarray or 2-tuple of ndarray
        索引的布尔数组, 或者两个下标数组构成的元组.

    Examples
    --------
    mask = region_ind(lon2d, lat2d, extents)
    data1d = data2d[mask]

    ixgrid = region_ind(lon1d, lat1d, extents, form='ix')
    data2d_subset = data2d[ixgrid]
    data3d_subset = data3d[:, ixgrid[0], ixgrid[1]]
    '''
    lon = np.asarray(lon)
    lat = np.asarray(lat)
    lonmin, lonmax, latmin, latmax = extents
    mask_lon = (lon >= lonmin) & (lon <= lonmax)
    mask_lat = (lat >= latmin) & (lat <= latmax)
    if form == 'mask':
        if lon.shape != lat.shape:
            raise ValueError('lon和lat的形状不匹配.')
        ind = mask_lon & mask_lat
    elif form == 'ix':
        ind = np.ix_(mask_lon, mask_lat)
    else:
        raise ValueError('form不支持')

    return ind

def interp_nearest(
    points: Any,
    values: Any,
    xi: Any,
    radius: float = np.inf,
    fill_value: float = np.nan
) -> np.ndarray:
    '''
    可以限制搜索半径的最近邻插值.

    Parameters
    ----------
    points : (n, d) array_like
        n个数据点的坐标, 每个点有d个坐标分量.

    values : (n,) or (k, n) array_like
        n个数据点的变量值, 可以有k个变量.

    xi: (m, d) array_like
        m个插值点的坐标. 每个点有d个坐标分量.

    radius : float, optional
        插值点能匹配到数据点的最大距离(半径). 默认为Inf.

    fill_value : float, optional
        距离超出radius的插值点用fill_value填充. 默认为NaN.

    Returns
    -------
    result : (m,) or (k, m) ndarray
        插值点处变量值的数组.
    '''
    points = np.asarray(points)
    xi = np.asarray(xi)
    values = np.asarray(values, dtype=float)

    # 利用KDTree搜索最邻近的值.
    tree = KDTree(points)
    dd, ii = tree.query(xi)
    result = values[..., ii]
    result[..., dd > radius] = fill_value

    return result

def bin_avg(
    x: Any,
    y: Any,
    data: Any,
    xbins: Any,
    ybins: Any
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    利用平均的方式对散点数据进行二维binning.

    Parameters
    ----------
    x : (n,) array_like
        n个数据点的横坐标.

    y : (n,) array_like
        n个数据点的纵坐标.

    data : (n,) or (m, n) array_like
        n个数据点的变量值, 可以有m个变量.

    xbins : (nx + 1,) array_like
        用于划分横坐标的bins.

    ybins : (ny + 1,) array_like
        用于划分纵坐标的bins.

    Returns
    -------
    xc : (nx,) ndarray
        xbins每个bin中心的横坐标.

    yc : (ny,) ndarray
        ybins每个bin中心的纵坐标.

    avg : (ny, nx) or (m, ny, nx) ndarray
        xbins和ybins构成的网格内的变量平均值.
        为了便于画图, 采取(ny, nx)的形状.
    '''
    def nanmean(arr):
        '''避免空切片警告的nanmean.'''
        arr = arr[~np.isnan(arr)]
        return np.nan if arr.size == 0 else arr.mean()

    avg, xbins, ybins, _ = binned_statistic_2d(
        x, y, data,
        bins=[xbins, ybins],
        statistic=nanmean
    )
    xc = (xbins[1:] + xbins[:-1]) / 2
    yc = (ybins[1:] + ybins[:-1]) / 2

    return xc, yc, avg