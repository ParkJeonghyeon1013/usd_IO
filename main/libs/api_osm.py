import hou as hou

class OSMCity:
    def __init__(self):
        pass

    @staticmethod
    def create_hip():
        # init HOUDINI
        hou.hipFile.clear(suppress_save_prompt=True)




        # set frame range
        start_frame = 1001
        end_frame = 1010
        hou.setFps(int(24))
        globFrameSetExpr = "tset `({0}-1)/$FPS` `{1}/$FPS`".format(int(start_frame), int(end_frame))
        hou.hscript(globFrameSetExpr)
        hou.playbar.setPlaybackRange(int(start_frame), int(end_frame))
        n_obj = hou.node("/obj")

    @staticmethod
    def default_set(osm_file='D:/git_workspace/usd_IO/hip_practice/based_osm/osm_img/mokdong.osm'):
        obj = hou.node('/obj')
        n_geo = obj.createNode("geo")

        n_osm_import = n_geo.createNode('labs::osm_import')
        n_osm_import.parm('osm_file').set(osm_file)

        n_osm_filter = n_geo.createNode('labs::osm_filter')
        n_osm_filter.setInput(0, n_osm_import)

        n_osm_building = n_geo.createNode('labs::osm_buildings')
        n_osm_building.parm('gen_nodata').set(1)
        n_osm_building.setInput(0, n_osm_filter)

        n_xform = n_geo.createNode('xform')
        n_xform.parm('ry').setExpression('$F')
        n_xform.parm('px').setExpression("centroid(0, D_X)")
        n_xform.parm('py').setExpression("centroid(0, D_Y)")
        n_xform.parm('pz').setExpression("centroid(0, D_Z)")
        n_xform.setInput(0, n_osm_building)

    @staticmethod
    def save_hip(hip_path):
        # hip save
        hou.hipFile.save(hip_path)

if __name__ == '__main__':
    pass
