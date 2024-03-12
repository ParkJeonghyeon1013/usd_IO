import sys, os
import re, importlib, subprocess
import hou as hou

class GrayScaleCity:
    def __init__(self):
        self.version = 0
        pass

    # 노드 생성 시 위치 정렬을 위한 메서드
    def align_node_pos(self, node_name, node_pos, add_x, add_y):
        node_name.setPosition((node_pos[0] + add_x, node_pos[1] + add_y))

    @staticmethod
    def set_hipfile():
        # init HOUDINI
        hou.hipFile.clear(suppress_save_prompt=True)


        # set frame range - 5s [1001-1121]

        start_frame = 1001
        end_frame = 1120
        hou.setFps(int(24))
        frame_set = f"`{start_frame -1}/$FPS` `{end_frame}/$FPS`"
        hou.hscript(frame_set)
        hou.playbar.setPlaybackRange(int(start_frame), int(end_frame))



    def create_mov(self):

        pass



    def create_jpg(self):
        pass



    def save_hip(self, dir_path):
        hip_path = os.path.join(dir_path, f'grayscale.{self.version}.hip')
        # hip save
        hou.hipFile.save(hip_path)
        self.version += 1


    def create_city(self):

        # Create Main Node
        obj = hou.node("/obj")

        n_street_grid = obj.createNode("geo", "STREET_GRID")
        n_work_viewer1 = obj.createNode("geo", "WORK_Building_VIEWER1")
        n_work_viewer2 = obj.createNode("geo", "WORK_Building_VIEWER2")
        n_render_viewer1= obj.createNode("geo", "RENDER_Building_VIEWER1")
        n_render_viewer2= obj.createNode("geo", "RENDER_Building_VIEWER2")
        n_topnet = obj.createNode("topnet")

        n_topnet.setPosition([4, 0])
        n_work_viewer1.setPosition([0, -1])
        n_work_viewer2.setPosition([0, -2])
        n_render_viewer1.setPosition([4, -1])
        n_render_viewer2.setPosition([4, -2])

######################################################################################################################
        # n_work_viewer1 노드 안에 file 노드 생성 후 값 세팅
        file_node = n_work_viewer1.createNode("file")
        file_node.parm("file").set("`@pdg_output`")

######################################################################################################################
        # obj > street_grid > subnet
        # TODO : grid size / path 설정하기!!!!!!!!!!!!!!! 일단 절대로 두고, 상대로 변경은 나중에!!!!!!!!!
        n_subnet = n_street_grid.createNode("subnet", "streetgrid_maker")
        n_trace = n_subnet.createNode("trace")

        n_trace.parm("rx").set(-90)
        n_trace.parm("ry").setExpression('($F/$FEND)*2000')
        n_trace.parm("sx").set(100)
        trace_sx = n_trace.parm("sx")
        n_trace.parm("sy").set(trace_sx)

        # n_trace.parm("file").set("/home/rapa/git_workspace/usd_IO/hip_practice/script_grayscale/tex/citygrid.jpg") # grid 이미지 경로 설정
        n_trace.parm("file").set("D:/git_workspace/usd_IO/hip_practice/script_grayscale/tex/citygrid.jpg") # grid 이미지 경로 설정
        n_trace.parm("overridesize").set(1)     # gird size 랑 그냥 relative로 엮어줄까?
        n_trace.parm("imagesize1").set(500)
        n_trace.parm("imagesize2").set(500)

        n_reverse = n_subnet.createNode("reverse")
        n_reverse.setInput(0, n_trace)
        self.align_node_pos(n_reverse, n_trace.position(), 0, -1)

        n_resample = n_subnet.createNode("resample")
        n_resample.setInput(0, n_reverse)
        self.align_node_pos(n_resample, n_reverse.position(), 0, -1)


        n_color = n_subnet.createNode("color")
        n_color.setInput(0, n_resample)
        # n_color.setColor(hou.Color(0,0,0))
        n_color.parm("colorr").set(0)
        n_color.parm("colorg").set(0)
        n_color.parm("colorb").set(0)
        n_color.parm("class").set(1)
        self.align_node_pos(n_color, n_resample.position(), 0, -1)


        # city core 제작 위함 = 초록색으로 표시 후 해당 부분을 추출하여 height를 높여주는 원리
        n_sphere = n_subnet.createNode("sphere")
        n_sphere.parm("type").set(1)
        n_sphere.parm("radx").set(0.5)
        n_sphere.parm("rady").set(0.5)
        n_sphere.parm("radz").set(0.5)
        n_sphere.parm("scale").set(5)
        self.align_node_pos(n_sphere, n_trace.position(), 3, -1)


        n_sphere_color = n_subnet.createNode("color")
        n_sphere_color.parm("colorr").set(0)
        n_sphere_color.parm("colorg").set(1)
        n_sphere_color.parm("colorb").set(0)
        n_sphere_color.parm("class").set(1)
        n_sphere_color.setInput(0, n_sphere)
        self.align_node_pos(n_sphere_color, n_sphere.position(), 0, -1)


        n_attribute_transfer = n_subnet.createNode("attribtransfer")
        n_attribute_transfer.setInput(0, n_color)
        n_attribute_transfer.setInput(1, n_sphere_color)
        n_attribute_transfer.parm("pointattribs").set(0)
        n_attribute_transfer.parm("primattriblist").set("Cd")
        n_attribute_transfer.parm("thresholddist").set(0)
        n_attribute_transfer.parm("blendwidth").set(30)
        self.align_node_pos(n_attribute_transfer, n_sphere_color.position(), 0, -2)

        n_output = n_subnet.createNode("output")
        n_output.setInput(0, n_attribute_transfer)
        # n_output.setDisplayFlag(True)
        self.align_node_pos(n_output, n_attribute_transfer.position(), 0, -1)



        ##########################################################################################################

        # subnet을 통해서 HDA를 만들 때 relative로 parmeter 연결해주기 위한 작업!
        # ptg 그룹이 있다. 여기에 넣어주기 위한 parm templete 제작 > ptg 그룹에 넣어주고 > subnet에 set해주면 됨
        ptg = n_subnet.parmTemplateGroup()

        # 이 방식으로 hide 시켜줄 수 있음.
        # for i in ptg.parmTemplates():
        #     ptg.hide(i, True)
        # n_subnet.setParmTemplateGroup(ptg)

        template1 = hou.FloatParmTemplate(name='sx', label='Scale', num_components=2)
        template2 = hou.FloatParmTemplate(name='t', label='Sphere_Center', num_components=3)
        template3 = hou.FloatParmTemplate(name='blendwidth', label='Blend_Width', num_components=1)
        template4 = hou.StringParmTemplate(name='file', label='Image_input', num_components=1)
        # template5 = hou.StringParmTemplate(name='file', label='Image_input',  num_components=3, string_type=hou.stringParmType.FileReference,file_type=hou.fileType.Image)


        # ptg.parmTemplates()
        ptg.addParmTemplate(template1)
        ptg.addParmTemplate(template2)
        ptg.addParmTemplate(template3)
        ptg.addParmTemplate(template4)
        # ptg.addParmTemplate(template5)

        n_subnet.setParmTemplateGroup(ptg)


        # TODO ::::::::::: parm과 relative로 연결하기
        # n_subnet.parm("file").setExpression('`chs("trace1/file")`')
        '''
        // image input (file) : subnet > trace > image input
        // scale X (sx) : subnet > trace > scale X
        // sphere center : subnet > sphere > center
        // blend width : subnet > attribtransfer > blend width 
        '''


        # obj > STREET_GRID
        # houdini asset 만들기
        hda_grid = hou.node('/obj/STREET_GRID/streetgrid_maker')
        # node = hda_grid.createDigitalAsset(name='Street_maker', hda_file_name='/home/rapa/git_workspace/usd_IO/hip_practice/script_grayscale/hda/streetgrid_maker.hda')
        node = hda_grid.createDigitalAsset(name='Street_maker', hda_file_name='D:/git_workspace/usd_IO/output/streetgrid_maker.hdanc')


        # null 생성해서 연결
        n_subnet = hou.node('/obj/STREET_GRID/streetgrid_maker')
        n_null = n_street_grid.createNode("null", "CITYBLOCKS_OUT")
        n_null.setInput(0, n_subnet)
        self.align_node_pos(n_null, n_subnet.position(), 0, -1)

##########################################################################################################
        # obj > topnet > localscheduler
        n_localscheduler = n_topnet.node('localscheduler')
        n_localscheduler.parm('maxprocsmenu').set(-1)


        # topnet 작업 > wedge 노드 세팅
        # 몇 가지의 variation 줄지 설정
        n_wedge = n_topnet.createNode("wedge")
        n_wedge.setPosition([0, -1])
        n_wedge.parm("wedgecount").set(4)
        n_wedge.parm("wedgeattributes").set(3)

        # attribute 1 = center_wedge
        n_wedge.parm("name1").set("center_wedge")
        n_wedge.parm("type1").set(1)
        n_wedge.parm("random1").set(1)
        n_wedge.parm("floatrangestart1x").set(-50)
        n_wedge.parm("floatrangestart1y").set(0)
        n_wedge.parm("floatrangestart1z").set(-50)
        n_wedge.parm("floatrangestart1w").set(0)

        n_wedge.parm("floatrangeend1x").set(50)
        n_wedge.parm("floatrangeend1y").set(0)
        n_wedge.parm("floatrangeend1z").set(50)
        n_wedge.parm("floatrangeend1w").set(0)


        # attribute 2 = seed_wedge
        n_wedge.parm("name2").set("seed_wedge")
        n_wedge.parm("type2").set(0)
        n_wedge.parm("random2").set(1)
        n_wedge.parm("floatrange2x").set(0)
        n_wedge.parm("floatrange2y").set(1000)


        # attribute 3 = file_wedge
        n_wedge.parm("name3").set("file_wedge")
        n_wedge.parm("type3").set(0)
        n_wedge.parm("random3").set(0)
        n_wedge.parm("floatrange3x").set(1)
        n_wedge.parm("floatrange3y").set(4)


        # hdaProcessor 1 = make_cirygrid
        # Write file location and Just call callback func

        n_hdaprocessor = n_topnet.createNode("hdaprocessor")
        n_hdaprocessor.setInput(0, n_wedge)
        n_hdaprocessor.setName("make_citygrid")
        # n_hdaprocessor.parm("inputfile").set("$HIP/hda/streetgrid_maker.hdanc")
        n_hdaprocessor.parm("inputfile").set("D:/git_workspace/usd_IO/output/streetgrid_maker.hdanc")
        self.align_node_pos(n_hdaprocessor, n_wedge.position(), 0, -1)

        # NEEEEEEEEDDDDDDD to fix
        # PPPPPPPPPPPPPPPPPRRRRRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOO blem~~~~~~~~~~~~~~~~~~~~~~~
        # n_hdaprocessor.parm("operatortype").set("Sop/USER::streetgrid_maker::1.0")
        # n_hdaprocessor.parm("hdatype").set(1)
        # n_hdaprocessor.parm("outputfile1").set("$HIP/geo/$OS.`@pdg_name`.`@wedgenum`.0.bgeo.sc")
        # n_hdaprocessor.parm("outputtag1").set("file/geo")
        # n_hdaprocessor.parm("updateHDAParms").set(1)

        # delete upper things. cause callback method fill everything
        # todo::::::::::::::: 근데 윈도우에서 해보니까 안됨...
        # n_hdaprocessor.hdaModule().hdaFileChanged({'node':n_hdaprocessor})
        # n_hdaprocessor.parm("hdap_tx").setExpression("@center_wedge.0")
        # n_hdaprocessor.parm("hdap_ty").setExpression("@center_wedge.1")
        # n_hdaprocessor.parm("hdap_tz").setExpression("@center_wedge.2")


        # TODO: PUT relative parms to HDA parameters
        # image input은 연결되어있음! 그리드 사이즈는 고정되어있어서 image 사이즈가 커지면 grid (= 도시 사이즈) 도 함께 커질 수 있게 만들어주기



        # obj > topnet > geometryimport
        n_geometryimport = n_topnet.createNode("geometryimport", "cityblocks")
        # n_geometryimport.setName("cityblocks")
        n_geometryimport.parm("geometrysource").set(0)
        n_geometryimport.parm("pdg_workitemgeneration").set(0)
        n_geometryimport.parm("geometrysource").set(1)
        n_geometryimport.parm("externalpath").set("$HIP/geo/$HIPNAME.$OS.`@pdg_index`.`@wedgenum`.bgeo.sc")
        n_geometryimport.parm("class").set(2)
        n_geometryimport.setInput(0, n_hdaprocessor)
        self.align_node_pos(n_geometryimport, n_hdaprocessor.position(), 0, -1)


        # obj > topnet > attributecreate1 = attr_core
        n_att_create1 = n_topnet.createNode("attributecreate", "attributecreate_core")
        n_att_create1.parm("pdg_workitemgeneration").set(0)
        n_att_create1.parm("floatattribs").set(2)




        n_att_create1.parm("floatname1").set("base_height")
        n_att_create1.parm("floatvalue11").set(10)
        n_att_create1.parm("floatname2").set("height_variation")
        n_att_create1.parm("floatvalue21").setExpression("rand(@pdg_index*@seed_wedge)*15 + @Cd.g*30")
        n_att_create1.setInput(0, n_geometryimport)
        self.align_node_pos(n_att_create1, n_geometryimport.position(), 0, -1)


        # obj > topnet > attributecreate2 = attr_isolate
        n_att_create2 = n_topnet.createNode("attributecreate", "attributecreate_isolate")
        n_att_create2.parm("usecondition").set(1)
        # todo!!!!!!!!!!!!!!!!!!!! ADD create when expresssion

        n_att_create2.parm("floatattribs").set(2)
        n_att_create2.parm("floatname1").set("base_heigiht")
        n_att_create2.parm("floatvalue11").set(50)
        n_att_create2.parm("floatname2").set("height_variation")
        n_att_create2.setInput(0, n_att_create1)
        self.align_node_pos(n_att_create2, n_att_create1.position(), 0, -1)


        n_rop_geo = n_topnet.createNode("ropgeometry")
        n_rop_geo.setName("create_buildings")
        n_rop_geo.parm("usesoppath").set(0)
        n_rop_geo.parm("sopoutput").set("$HIP/geo/$HIPNAME.$OS.`@pdg_index`.`@wedgenum`.bgeo.sc")
        n_rop_geo.parm("pdg_cachemode").set(2)
        n_rop_geo.parm("pdg_cooktype").set(3)
        n_rop_geo.setInput(0, n_att_create2)
        self.align_node_pos(n_rop_geo, n_att_create2.position(), 0, -1)

#########################################################################################################################
        # obj > topnet > ropgeometry = create_building
        # ropgeometry 노드의 경우 Lock 이 걸려있어서 그런지 세부 경로를 타고 가야 했음.
        n_rop_in = hou.node(n_rop_geo.path()+'/s/s')
        n_out = hou.node('/obj/topnet1/create_buildings/s/s/output1')
        n_out.setInput(0, None)

        n_file = hou.node('/obj/topnet1/create_buildings/s/s/incoming')
        n_file.parm("file").set("`@pdg_input`")
        self.align_node_pos(n_out, n_file.position(), 0, -10)


        n_extrude1 = n_rop_in.createNode("polyextrude::2.0")
        n_extrude1.setName("block_offset")
        n_extrude1.parm("outputfront").set(1)
        n_extrude1.parm("outputback").set(0)
        n_extrude1.parm("outputside").set(0)
        n_extrude1.setInput(0, n_file)
        self.align_node_pos(n_extrude1, n_file.position(), 0, -1)

        n_fuse = n_rop_in.createNode("fuse")
        n_fuse.parm("tol3d").set(0.2)
        n_fuse.setInput(0, n_extrude1)
        self.align_node_pos(n_fuse, n_extrude1.position(), 0, -1)

        n_extrude2 = n_rop_in.createNode("polyextrude::2.0", "building_height")
        n_extrude2.parm("dist").setExpression("@base_height+@height_variation")
        n_extrude2.parm("divs").setExpression('ch("dist")/2')
        n_extrude2.parm("outputfrontgrp").set(1)
        n_extrude2.parm("outputsidegrp").set(1)
        n_extrude2.parm("frontgrp").set("building_top")
        n_extrude2.parm("sidegrp").set("building_side")
        n_extrude2.setInput(0, n_fuse)
        self.align_node_pos(n_extrude2, n_fuse.position(), 0, -1)

        n_extrude3 = n_rop_in.createNode("polyextrude::2.0", "window_frames")
        n_extrude3.parm("inset").set(0.05)
        n_extrude3.parm("group").set("building_side")
        n_extrude3.parm("splittype").set(0)
        n_extrude3.parm("outputfront").set(1)
        n_extrude3.parm("outputback").set(0)
        n_extrude3.parm("outputside").set(1)
        n_extrude3.parm("outputfrontgrp").set(1)
        n_extrude3.parm("frontgrp").set("window_out")
        n_extrude3.setInput(0, n_extrude2)
        self.align_node_pos(n_extrude3, n_extrude2.position(), 0, -1)

        n_extrude4 = n_rop_in.createNode("polyextrude::2.0", "window")
        n_extrude4.parm("dist").set(-0.05)
        n_extrude4.parm("group").set("window_out")
        n_extrude4.setInput(0, n_extrude3)
        self.align_node_pos(n_extrude4, n_extrude3.position(), 0, -1)

        n_extrude5 = n_rop_in.createNode("polyextrude::2.0", "extend_roof")
        n_extrude5.parm("group").set("building_top")
        n_extrude5.parm("dist").set(0.5)
        n_extrude5.setInput(0,n_extrude4)
        self.align_node_pos(n_extrude5, n_extrude4.position(), 0, -1)

        n_extrude6 = n_rop_in.createNode("polyextrude::2.0")
        n_extrude6.setName("roof_edge")
        n_extrude6.parm("group").set("building_top")
        n_extrude6.parm("inset").set(0.3)
        n_extrude6.parm("outputfront").set(1)
        n_extrude6.parm("outputback").set(0)
        n_extrude6.parm("outputside").set(1)
        n_extrude6.parm("outputfrontgrp").set(1)
        n_extrude6.parm("frontgrp").set("roof_out")
        n_extrude6.setInput(0, n_extrude5)
        self.align_node_pos(n_extrude6, n_extrude5.position(), 0, -1)

        n_extrude7 = n_rop_in.createNode("polyextrude::2.0", "roof_edge_in")
        n_extrude7.parm("group").set("roof_out")
        n_extrude7.parm("dist").set(-0.25)
        n_extrude7.setInput(0, n_extrude6)
        self.align_node_pos(n_extrude7, n_extrude6.position(), 0, -1)

        n_color = n_rop_in.createNode("color")
        n_color.parm("group").set("window_out")
        n_color.parm("colorr").set(0)
        n_color.parm("colorg").set(0)
        n_color.parm("colorb").set(0)
        n_color.setInput(0, n_extrude7)
        self.align_node_pos(n_color, n_extrude7.position(), 0, -1)

        n_out.setInput(0, n_color)

##########################################################################################################################
        # obj > topnet > partitionbyatrribute
        n_part_att = n_topnet.createNode("partitionbyattribute")
        n_part_att.parm("attributes").set(1)
        n_part_att.parm("name1").set("wedgenum")
        n_part_att.setInput(0, n_rop_geo)
        self.align_node_pos(n_part_att, n_rop_geo.position(), 0, -1)

        # obj > topnet > geometryimport
        n_rop_geo2 = n_topnet.createNode("geometryimport", "building_merge")
        n_rop_geo2.parm("mergeinput").set(1)
        n_rop_geo2.parm("externalpath").set("$HIP/geo/$HIPNAME.$OS.`@pdg_index`.`@wedgenum`.bgeo.sc")
        n_rop_geo2.setInput(0, n_part_att)
        self.align_node_pos(n_rop_geo2, n_part_att.position(), 0, -1)

        # obj > topnet
        n_rop_import2 = n_topnet.createNode("ropgeometry", "build_streets")
        n_rop_import2.parm("usesoppath").set(0)
        n_rop_import2.parm("sopoutput").set("$HIP/geo/$HIPNAME.$OS.`@wedgenum`.bgeo.sc1")
        n_rop_import2.parm("pdg_cachemode").set(2)
        n_rop_import2.parm("pdg_cooktype").set(3)
        n_rop_import2.setInput(0, n_hdaprocessor)
        self.align_node_pos(n_rop_import2, n_geometryimport.position(), 4, 0)


        # obj > topnet > ropgeometryimport
        n_rop2_in = hou.node(n_rop_import2.path()+'/s/s')
        n_file2 = hou.node('/obj/topnet1/build_streets/s/s/incoming')
        n_out2 = hou.node('/obj/topnet1/build_streets/s/s/output1')
        n_out2.setInput(0, None)
        self.align_node_pos(n_out2, n_file2.position(), 0, -7)

        n2_extrude1 = n_rop2_in.createNode("polyextrude::2.0")
        n2_extrude1.parm("dist").set(-0.05)
        n2_extrude1.parm("outputfront").set(0)
        n2_extrude1.parm("outputback").set(1)
        n2_extrude1.parm("outputside").set(1)
        n2_extrude1.setInput(0, n_file2)
        self.align_node_pos(n2_extrude1, n_file2.position(), 0, -10)

        n2_reverse = n_rop2_in.createNode("reverse")
        n2_reverse.setInput(0, n2_extrude1)
        self.align_node_pos(n2_reverse, n2_extrude1.position(), 0, -1)

        n2_color = n_rop2_in.createNode("color")
        n2_color.setInput(0, n2_reverse)
        self.align_node_pos(n2_color, n2_reverse.position(), 0, -1)

        n2_merge = n_rop2_in.createNode("merge")
        n2_merge.setInput(0, n2_color)
        self.align_node_pos(n2_merge, n2_color.position(), 0, -1)

        n2_box = n_rop2_in.createNode("box")
        n2_box.parm("type").set(1)
        n2_box.parm("divrate1").set(2)
        n2_box.parm("divrate2").set(2)
        n2_box.parm("divrate3").set(2)
        n2_box.setInput(0, n2_extrude1)
        self.align_node_pos(n2_box, n2_extrude1.position(), 3, -1)

        n2_blast = n_rop2_in.createNode("blast")
        n2_blast.parm("group").set("2")
        n2_blast.parm("negate").set(1)
        n2_blast.setInput(0, n2_box)
        self.align_node_pos(n2_blast, n2_box.position(), 0, -1)


        n2_transform = n_rop2_in.createNode("xform")
        n2_transform.parm("ty").set(-0.05)
        n2_transform.parm("sx").set(1.05)
        n2_transform.parm("sy").set(1)
        n2_transform.parm("sz").set(1.05)
        n2_transform.setInput(0, n2_blast)
        self.align_node_pos(n2_transform, n2_blast.position(), 0, -1)


        n2_color2 = n_rop2_in.createNode("color")
        n2_color2.parm("colorr").set(0.33)
        n2_color2.parm("colorg").set(0.33)
        n2_color2.parm("colorb").set(0.33)
        n2_color2.setInput(0, n2_transform)
        self.align_node_pos(n2_color2, n2_transform.position(), 0, -1)

        n2_merge.setInput(1, n2_color2)
        n_out2.setInput(0, n2_merge)
        self.align_node_pos(n2_merge, n2_color.position(), 0, -3)

##########################################################################################
        # obj > topnet > patitionbyindex
        n_partition_idx = n_topnet.createNode("partitionbyindex")
        n_partition_idx.setInput(0, n_rop_geo2)
        n_partition_idx.setInput(1, n_rop_import2)
        self.align_node_pos(n_partition_idx, n_rop_geo2.position(), 0, -1)

###########################################################################################################
        # n_work_viewer2 노드 안에 file 노드 생성 후 값 세팅
        file_node = n_work_viewer2.createNode("file")
        file_node.parm("file").set("`@pdg_output.1`")

#####################################################################
        # display mode on 해주기
        n_topnet.cookAllOutputWorkItems(True)

        n_work_viewer1.setDisplayFlag(True)
        n_work_viewer2.setDisplayFlag(True)
        n_render_viewer1.setDisplayFlag(False)
        n_render_viewer2.setDisplayFlag(False)



################################################################dd##########################
# turntable setting
    def set_render(self, dir_path):
        # set Node variable
        obj = hou.node("/obj")

        n_street_grid = hou.node('/obj/STREET_GRID')
        n_work_viewer1 = hou.node('/obj/WORK_Building_VIEWER1')
        n_work_viewer2 = hou.node('/obj/WORK_Building_VIEWER2')
        n_render_viewer1 = hou.node('/obj/RENDER_Building_VIEWER1')
        n_render_viewer2 = hou.node('/obj/RENDER_Building_VIEWER2')
        n_topnet = hou.node('/obj/topnet1')

        n1_file_node = n_render_viewer1.createNode("file")
        n1_file_node.parm("file").set("`@pdg_input`")

        n2_file_node = n_render_viewer2.createNode("file")
        n2_file_node.parm("file").set("`@pdg_input.1`")

        jpg_path = os.path.join(dir_path, f'grayscale.{self.version}')

        # Render displayFlag set
        n_work_viewer1.setDisplayFlag(False)
        n_work_viewer2.setDisplayFlag(False)
        n_render_viewer1.setDisplayFlag(True)
        n_render_viewer2.setDisplayFlag(True)

        # camera/ light 세팅
        # TODO: :::::::::::::::::::: camera 위치 세팅
        n_cam = obj.createNode("cam")
        n_light1 = obj.createNode("hlight::2.0", "sunlight")
        n_light1.parm("light_type").set(8)
        n_light1.parm("vm_envangle").set(2)

        n_light2 = obj.createNode("envlight", "skylight")
        n_light2.parm("skymap_enable").set(1)
        n_light2.parm("light_intensity").set(1.3)
        self.align_node_pos(n_cam, n_work_viewer2.position(), 0, -1)
        self.align_node_pos(n_light1, n_cam.position(), 0, -1)
        self.align_node_pos(n_light2, n_light1.position(), 3, -1)

        # obj > topnet > mantra renderer 추가
        n_part_idx = hou.node("/obj/topnet1/partitionbyindex1")
        n_mantra = n_topnet.createNode("ropmantra")
        n_mantra.setInput(0, n_part_idx)
        n_mantra.parm("pdg_cachemode").set(2)
        n_mantra.parm("override_camerares").set(1)
        n_mantra.parm("vm_picture").set("$HIP/render/$HIPNAME.$OS.`@wedgenum`.png")
        self.align_node_pos(n_mantra, n_part_idx.position(), 0, -2)

        # obj > topnet > overlaytext
        n_overlaytext = n_topnet.createNode("ropcomposite")
        n_overlaytext.setInput(0, n_mantra)
        n_overlaytext.parm("copoutput").set("$HIP/render/$HIPNAME.$OS.`@wedgenum`.png")
        self.align_node_pos(n_overlaytext, n_mantra.position(), 0, -2)

        n_overlaytext_in = hou.node(n_overlaytext.path()+'/c')
        n_pdg_result = hou.node('/obj/topnet1/ropcomposite1/c/pdg_result')

        n_font = n_overlaytext_in.createNode("font")
        n_font.parm("text").set("Map: `@file_wedge`\nCity Core: `@center_wedge.0`, `@center_wedge.2`\nVariation Seed: `@seed_wedge`")
        n_font.parm("textsize").set(30)
        n_font.setInput(0, n_pdg_result)
        self.align_node_pos(n_font, n_pdg_result.position(), -2, -2)

        n_dropshadow = n_overlaytext_in.createNode("dropshadow")
        n_dropshadow.setInput(0, n_font)
        self.align_node_pos(n_dropshadow, n_font.position(), 0, -2)

        n_over = n_overlaytext_in.createNode("over")
        n_over.setInput(0, n_dropshadow)
        n_over.setInput(1, n_pdg_result)
        self.align_node_pos(n_over, n_dropshadow.position(), 2, -2)

        # obj > topnet > waitforall
        # n_wait = n_topnet.createNode("waitforall")
        # n_wait.setInput(0, n_overlaytext)
        # self.align_node_pos(n_wait, n_overlaytext.position(), 0, -2)
        #
        # n_magick = n_topnet.createNode("imagemagick")
        # n_magick.setInput(0, n_wait)
        # self.align_node_pos()
        #

        # todo ::::::::::: file save > topnet cook > render 순으로 진행
        #cook 해주고 render 해주기
        n_topnet.dirtyAllTasks(True)
        n_topnet.cookAllOutputWorkItems(True)





# when people wanna watch viewport -> topnet 에서 partitionby index 를 ouput으로 두고 recook 한 후 work viewer 로 보기


if __name__ == '__main__':
    pass


