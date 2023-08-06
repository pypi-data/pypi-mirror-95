from libc.math cimport sqrt
from libc.math cimport cos
from libc.math cimport sin
from libc.math cimport M_PI

cpdef list get_cartesian_coord(float lat, float lon, float h):
    """Convert coords from geodesic to cartesian."""
    cdef float a = 6378137.0
    cdef float rf = 298.257223563

    cdef float lat_rad = lat * M_PI/180
    cdef float lon_rad = lon * M_PI/180
    cdef float N = sqrt(a / (1 - (1 - (1 - 1 / rf) ** 2) * (sin(lat_rad)) ** 2))
    cdef float X = (N + h) * cos(lat_rad) * cos(lon_rad)
    cdef float Y = (N + h) * cos(lat_rad) * sin(lon_rad)
    cdef float Z = ((1 - 1 / rf) ** 2 * N + h) * sin(lat_rad)
    return [X, Y, Z]


cpdef float compute_dist(list p_1, list p_2):
    """Compute cartesian distance between points."""
    cdef float result = sqrt(
        (p_2[0] - p_1[0]) ** 2 + (p_2[1] - p_1[1]) ** 2 + (p_2[2] - p_1[2]) ** 2
    )
    return result


# cdef cy_cosine(np.ndarray[np.float64_t] x, np.ndarray[np.float64_t] y):
#     cdef double xx=0.0
#     cdef double yy=0.0
#     cdef double xy=0.0
#     cdef Py_ssize_t i
#     for i in range(len(x)):
#         xx+=x[i]*x[i]
#         yy+=y[i]*y[i]
#         xy+=x[i]*y[i]
#     return 1.0-xy/sqrt(xx*yy)

# def get_cartesian_coord(lat: float, lon: float, h: float) -> Sequence:
#     """Convert coords from geodesic to cartesian."""
#     a = 6378137.0
#     rf = 298.257223563
#     lat_rad = radians(lat)
#     lon_rad = radians(lon)
#     N = sqrt(a / (1 - (1 - (1 - 1 / rf) ** 2) * (sin(lat_rad)) ** 2))
#     X = (N + h) * cos(lat_rad) * cos(lon_rad)
#     Y = (N + h) * cos(lat_rad) * sin(lon_rad)
#     Z = ((1 - 1 / rf) ** 2 * N + h) * sin(lat_rad)
#     return X, Y, Z