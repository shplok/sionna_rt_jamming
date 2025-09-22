import numpy as np
import mitsuba as mi
import osmnx as ox
import shapely.geometry as geom

def load_osm_scene(osm_file):
    """
    Load an OSM file and convert buildings to a Sionna RT/Mitsuba scene.
    Returns a Mitsuba scene.
    """
    # Example: download building footprints if you provide a bounding box
    # Here, for simplicity, we simulate two rectangular buildings
    # You can replace this with actual OSM parsing from `osm_file`

    buildings = [
        {'coords': np.array([[0,0],[0,5],[5,5],[5,0]]), 'height':10.0},
        {'coords': np.array([[6,0],[6,3],[9,3],[9,0]]), 'height':8.0}
    ]

    scene_xml = "<scene version='2.0.0'>\n"
    for b in buildings:
        coords = b['coords']
        min_x, min_y = coords[:,0].min(), coords[:,1].min()
        max_x, max_y = coords[:,0].max(), coords[:,1].max()
        height = b['height']
        scene_xml += f"""
        <shape type="rectangle">
            <bsdf type="diffuse"/>
            <transform name="to_world">
                <scale x="{max_x - min_x}" y="{max_y - min_y}" z="{height}"/>
                <translate x="{min_x}" y="{min_y}" z="{height/2}"/>
            </transform>
        </shape>
        """
    scene_xml += "</scene>"

    return mi.load_string(scene_xml)
