#press command s when done to save the file,runnign the file will create a CAD.stl file in the same directory as this file.
# You can open it in a 3D viewer to see the cube in bamboo studio. 
# You can also import it into a slicer to print it on a 3D printer. 
# each time a CAD.stl file is created go into file editor, make a copy, and rename it,
# that way your cubes won't overwrite each other. 
# You can also change the name of the file in the code below, 
# but make sure to keep the .stl extension. each other time you run the code, 
# it will overwrite the CAD.stl file with the new dimensions. 
# You can also change the name of the file in the code below, but make sure to keep the .stl extension. 
# each other time you run the code, it will overwrite the CAD.stl file with the new dimensions."

from math import sqrt
def write_cube(path, width, depth, height):
    if min(width, depth, height) <= 0:
        raise ValueError("Dimensions must be greater than zero.")

    vertices = [
        (0, 0, 0),
        (width, 0, 0),
        (width, depth, 0),
        (0, depth, 0),
        (0, 0, height),
        (width, 0, height),
        (width, depth, height),
        (0, depth, height),
    ]

    faces = (
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (3, 7, 6, 2),
        (0, 4, 7, 3),
        (1, 2, 6, 5),
    )

    def subtract(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def clean_zero(val):
        return 0.0 if abs(val) < 1e-9 else val

    def normal(a, b, c):
        u = subtract(b, a)
        v = subtract(c, a)
        nx = u[1] * v[2] - u[2] * v[1]
        ny = u[2] * v[0] - u[0] * v[2]
        nz = u[0] * v[1] - u[1] * v[0]
        length = sqrt(nx * nx + ny * ny + nz * nz)
        return (
            clean_zero(nx / length),
            clean_zero(ny / length),
            clean_zero(nz / length),
        )

    with open(path, "w", encoding="ascii", newline="\n") as stl:
        stl.write("solid calibration_cube\n")
        for face in faces:
            triangles = [
                (face[0], face[1], face[2]),
                (face[0], face[2], face[3]),
            ]
            for i1, i2, i3 in triangles:
                a, b, c = vertices[i1], vertices[i2], vertices[i3]
                nx, ny, nz = normal(a, b, c)
                stl.write(f"  facet normal {nx:.6f} {ny:.6f} {nz:.6f}\n")
                stl.write("    outer loop\n")
                for x, y, z in (a, b, c):
                    stl.write(
                        f"      vertex {clean_zero(x):.6f} {clean_zero(y):.6f} {clean_zero(z):.6f}\n"
                    )
                stl.write("    endloop\n")
                stl.write("  endfacet\n")
        stl.write("endsolid calibration_cube\n")


if __name__ == "__main__":
    print("Enter dimensions for your 3D model:")
    w = float(input("Width (mm): "))
    d = float(input("Depth (mm): "))
    h = float(input("Height (mm): "))

    write_cube("CAD.stl", w, d, h)
    print("Success! CAD.stl updated with your custom dimensions.")
