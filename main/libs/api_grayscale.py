import sys, os
import re, importlib, subprocess
import hou as hou

class GrayScaleCity:
    def __init__(self):
        pass




    def create_hip(self):
        pass

    def create_mov(self):

        pass

    def create_jpg(self):
        pass



obj = hou.node('/obj')

# 노드 생성
# def set_obj():
obj.createNode('geo')
obj.createNode('geo')
obj.createNode('geo')
obj.createNode('geo')
obj.createNode('geo')
obj.createNode('topnet')

# 노드 이름 변경
# def change_node_name():
n_street_grid = obj.node('geo1')
n_street_grid.setName('STREET_GRID')

n_work_viewer1 = obj.node('geo2')
n_work_viewer1.setName('WORK_Building_VIEWER1')

n_work_viewer2 = obj.node('geo3')
n_work_viewer2.setName('WORK_Street_VIEWER2')

n_render_viewer1 = obj.node('geo4')
n_render_viewer1.setName('RENDER_Building_VIEWER1')

n_render_viewer2 = obj.node('geo5')
n_render_viewer2.setName('RENDER_Street_VIEWER2')



#################################################################################################################################################
# n_work_viewer1 노드 안에 file 노드 생성 후 값 세팅
# def n_work_viewer():
file_node = n_work_viewer1.createNode('file1')
file_node.parm("file").set("`@pdg_output`")


########################################################################################################################################
# obj > street_grid > subnet
n_subnet = n_street_grid.createNode("subnet")
n_trace = n_subnet.createNode("trace")
n_trace.parm("rx").set(-90)
n_trace.parm("sx").set(100)
trace_sx = n_trace.parm("sx")
n_trace.parm("sy").set(trace_sx)
n_trace.parm("file").set("/home/rapa/git_workspace/usd_IO/hip_practice/script_grayscale/tex/citygrid.jpg") # grid 이미지 경로 설정
n_trace.parm("overridesize").set(1)
n_trace.parm("imagesize1").set(500)
n_trace.parm("imagesize2").set(500)


n_reverse = n_subnet.createNode("reverse")
n_reverse.setInput(0, n_trace)


n_resample = n_subnet.createNode("resample")
n_resample.setInput(0, n_reverse)

n_color = n_subnet.createNode("color")
n_color.setInput(0, n_resample)
# n_color.setColor(hou.Color(0,0,0))
n_color.parm("colorr").set(0)
n_color.parm("colorg").set(0)
n_color.parm("colorb").set(0)
n_color.parm("class").set(1)

n_sphere = n_subnet.createNode("sphere")
n_sphere.parm("type").set(1)
n_sphere.parm("radx").set(0.5)
n_sphere.parm("rady").set(0.5)
n_sphere.parm("radz").set(0.5)
n_sphere.parm("scale").set(5)

n_sphere_color = n_subnet.createNode("color")
n_sphere_color.parm("colorr").set(0)
n_sphere_color.parm("colorg").set(1)
n_sphere_color.parm("colorb").set(0)
n_sphere_color.parm("class").set(1)
n_sphere_color.setInput(0, n_sphere)

n_attribute_transfer = n_subnet.createNode("attribtransfer")
n_attribute_transfer.setInput(0, n_color)
n_attribute_transfer.setInput(1, n_sphere_color)
n_attribute_transfer.parm("pointattribs").set(0)
n_attribute_transfer.parm("primattriblist").set("Cd")
n_attribute_transfer.parm("thresholddist").set(0)
n_attribute_transfer.parm("blendwidth").set(30)

n_output = n_subnet.createNode("output")
n_output.setInput(0, n_attribute_transfer)

n_subnet.setName("streetgrid_maker")
n_street_grid.createNode("null")

ptg = n_subnet.parmTemplateGroup()
template1 = hou.FloatParmTemplate(name='sx', label='Scale', num_components=2)
template2 = hou.FloatParmTemplate(name='t', label='Sphere_Center', num_components=3)
template3 = hou.FloatParmTemplate(name='blendwidth', label='Blend_Width', num_components=1)
template4 = hou.StringParmTemplate(name='file', label='Image_input', num_components=1)
# ptg.parmTemplates()
ptg.addParmTemplate(template1)
ptg.addParmTemplate(template2)
ptg.addParmTemplate(template3)
ptg.addParmTemplate(template4)

# 이 방식으로 hide 시켜줄 수 있음.
n_subnet.setParmTemplateGroup(ptg)
for i in ptg:
    ptg.hide(i, True)
n_subnet.setParmTemplateGroup(ptg)



##########################################################################################################
# obj > STREET_GRID
# houdini asset 만들기
# hou.Node.createDigitalAsset(n_subnet)
hda_grid = hou.node('/obj/STREET_GRID/streetgrid_maker')
node = hda_grid.createDigitalAsset(name='Street_maker', hda_file_name='/home/rapa/git_workspace/usd_IO/hip_practice/script_grayscale/hda/streetgrid_maker.hda')




# null 생성해서 연결
n_street_grid.createNode("null")
null = n_street_grid.createNode("null")
null.setName("CITYBLOCKS_OUT")
null.setInput(0, n_subnet)



##########################################################################################################

# topnet 작업 > wedge 노드 세팅
# def topnet_wedge():
topnet = obj.node('topnet1')
wedge = topnet.node('wedge1')
wedge.parm("wedgecount").set(4)
wedge.parm("wedgeattributes").set(3)

# attribute 1 = center_wedge
wedge.parm("name1").set("center_wedge")
wedge.parm("type1").set(1)
wedge.parm("random1").set(1)
wedge.parm("floatrangestart1x").set(-50)
wedge.parm("floatrangestart1y").set(0)
wedge.parm("floatrangestart1z").set(-50)
wedge.parm("floatrangestart1w").set(0)

wedge.parm("floatrangeend1x").set(50)
wedge.parm("floatrangeend1y").set(0)
wedge.parm("floatrangeend1z").set(50)
wedge.parm("floatrangeend1w").set(0)


# attribute 2 = seed_wedge
wedge.parm("name2").set("seed_wedge")
wedge.parm("type2").set(0)
wedge.parm("random2").set(1)
wedge.parm("floatrange2x").set(0)
wedge.parm("floatrange2y").set(1000)


# attribute 3 = file_wedge
wedge.parm("name3").set("file_wedge")
wedge.parm("type3").set(0)
wedge.parm("random3").set(0)
wedge.parm("floatrange3x").set(1)
wedge.parm("floatrange3y").set(4)




# obj > topnet > localscheduler
n_localscheduler = topnet.node('localscheduler')
n_localscheduler.parm('maxprocsmenu').set(-1)


# hdaProcessor 1 = make_cirygrid
# TODO : QA ) 얘는 나중에 grid 기준으로 city 생성되면 할 수 있음. citygrid_maker HDA 만든거 사용하기 위함인데,, 아직 경로 지정하는 방법을 모르겠음.
# Write file location and Just call callback func
topnet.createNode("hdaprocessor")
n_hdaprocessor = topnet.node("hdaprocessor1")
n_hdaprocessor.setInput(0, wedge)
n_hdaprocessor.setName("make_citygrid")
n_hdaprocessor.parm("inputfile").set("$HIP/hda/streetgrid_maker.hdanc")
# n_hdaprocessor.parm("operatortype").set("Sop/USER::streetgrid_maker::1.0")
# n_hdaprocessor.parm("hdatype").set(1)
# n_hdaprocessor.parm("outputfile1").set("$HIP/geo/$OS.`@pdg_name`.`@wedgenum`.0.bgeo.sc")
# n_hdaprocessor.parm("outputtag1").set("file/geo")
# n_hdaprocessor.parm("updateHDAParms").set(1)

# delete upper things. cause callback fixed everything
n_hdaprocessor.hdaModule().hdaFileChanged({'node':n_hdaprocessor})
n_hdaprocessor.parm("hdap_tx").setExpression("@center_wedge.0")
n_hdaprocessor.parm("hdap_ty").setExpression("@center_wedge.1")
n_hdaprocessor.parm("hdap_tz").setExpression("@center_wedge.2")


# TODO: PUT relative parms to HDA parameters
# image input은 연결되어있음! 그리드 사이즈는 고정되어있어서 image 사이즈가 커지면 grid (= 도시 사이즈) 도 함께 커질 수 있게 만들어주기







# obj > topnet > geometryimport
n_geometryimport = topnet.createNode('geometryimport')
n_geometryimport.setName("cityblocks")
n_geometryimport.parm("geometrysource").set(0)
n_geometryimport.parm("pdg_workitemgeneration").set(0)
n_geometryimport.parm("geometrysource").set(1)
n_geometryimport.parm("externalpath").set("$HIP/geo/$HIPNAME.$OS.`@pdg_index`.`@wedgenum`.bgeo.sc")
n_geometryimport.parm("class").set(2)
n_geometryimport.setInput(0, n_hdaprocessor)



# obj > topnet > attributecreate1 = attr_core
n_att_create1 = topnet.createNode("attributecreate")
n_att_create1.setName("attributecreate_core")
n_att_create1.parm("pdg_workitemgeneration").set(0)
n_att_create1.parm("floatattribs").set(2)

n_att_create1.parm("floatname1").set("base_height")
n_att_create1.parm("floatvalue11").set(10)
n_att_create1.parm("floatname2").set("height_variation")
n_att_create1.parm("floatvalue21").setExpression("rand(@pdg_index*@seed_wedge)*15 + @Cd.g*30")
n_att_create1.setInput(0, n_geometryimport)


# obj > topnet > attributecreate2 = attr_isolate
n_att_create2 = topnet.createNode("attributecreate")
n_att_create2.setName("attributecreate_isolate")
n_att_create2.parm("usecondition").set(1)
# todo!!!!!!!!!!!!!!!!!!!! ADD create when expresssion

n_att_create2.parm("floatattribs").set(2)
n_att_create2.parm("floatname1").set("base_heigiht")
n_att_create2.parm("floatvalue11").set(50)
n_att_create2.parm("floatname2").set("height_variation")
n_att_create2.setInput(0, n_att_create1)

n_rop_geo = topnet.createNode("ropgeometry")
n_rop_geo.setName("create_buildings")
n_rop_geo.parm("usesoppath").set(0)
n_rop_geo.parm("sopoutput").set("$HIP/geo/$HIPNAME.$OS.`@pdg_index`.`@wedgenum`.bgeo.sc")
n_rop_geo.parm("pdg_cachemode").set(2)
n_rop_geo.parm("pdg_cooktype").set(3)
n_rop_geo.setInput(0, n_att_create2)


# obj > topnet > ropgeometry = create_building
# ropgeometry 노드의 경우 Lock 이 걸려있어서 그런지 세부 경로를 타고 가야 했음.
n_rop_in = hou.node(n_rop_geo.path()+'/s/s')
n_out = hou.node('/obj/topnet1/create_building/s/s/output1')
n_out.setInput(0, None)

n_file = hou.node('/obj/topnet1/create_building/s/s/incoming')
n_file.parm("file").set("`@pdg_input`")


n_extrude1 = n_rop_in.createNode("polyextrude::2.0")
n_extrude1.setName("block_offset")
n_extrude1.parm("outputfront").set(1)
n_extrude1.parm("outputback").set(0)
n_extrude1.parm("outputside").set(0)
n_extrude1.setInput(0, n_file)


n_fuse = n_rop_in.createNode("fuse")
n_fuse.parm("tol3d").set(0.2)
n_fuse.setInput(0, n_extrude1)


n_extrude2 = n_rop_in.createNode("polyextrude::2.0")
n_extrude2.setName("building_height")
n_extrude2.parm("dist").setExpression("@base_height+@height_variation")
n_extrude2.parm("divs").setExpression('ch("dist")/2')
n_extrude2.parm("outputfrontgrp").set(1)
n_extrude2.parm("outputsidegrp").set(1)
n_extrude2.parm("frontgrp").set("building_top")
n_extrude2.parm("sidegrp").set("building_side")
n_extrude2.setInput(0, n_fuse)

n_extrude3 = n_rop_in.createNode("polyextrude::2.0")
n_extrude3.setName("window_frames")
n_extrude3.parm("inset").set(0.05)
n_extrude3.parm("group").set("building_side")
n_extrude3.parm("splittype").set(0)
n_extrude3.parm("outputfront").set(1)
n_extrude3.parm("outputback").set(0)
n_extrude3.parm("outputside").set(1)
n_extrude3.parm("outputfrontgrp").set(1)
n_extrude3.parm("frontgrp").set("window_out")
n_extrude3.setInput(0, n_extrude2)

n_extrude4 = n_rop_in.createNode("polyextrude::2.0")
n_extrude4.setName("window")
n_extrude4.parm("dist").set(-0.05)
n_extrude4.parm("group").set("window_out")
n_extrude4.setInput(0, n_extrude3)

n_extrude5 = n_rop_in.createNode("polyextrude::2.0")
n_extrude5.setName("extend_roof")
n_extrude5.parm("group").set("building_top")
n_extrude5.parm("dist").set(0.5)
n_extrude5.setInput(0,n_extrude4)


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


n_extrude7 = n_rop_in.createNode("polyextrude::2.0")
n_extrude7.setName("roof_edge_in")
n_extrude7.parm("group").set("roof_out")
n_extrude7.parm("dist").set(-0.25)
n_extrude7.setInput(0, n_extrude6)


n_color = n_rop_in.createNode("color")
n_color.parm("group").set("window_out")
n_color.parm("colorr").set(0)
n_color.parm("colorg").set(0)
n_color.parm("colorb").set(0)
n_color.setInput(0, n_extrude7)

n_out = hou.node('/obj/topnet1/create_building/s/s/output1')
n_out.setInput(0, n_color)



# obj > topnet > partitionbyatrribute
n_part_att = topnet.createNode("partitionbyattribute")
n_part_att.parm("attributes").set(1)
n_part_att.parm("name1").set("wedgenum")
n_part_att.setInput(0, n_rop_geo)


# obj > topnet > geometryimport
n_rop_geo2 = topnet.createNode("geometryimport")
n_rop_geo2.setName("building_merge")
n_rop_geo2.parm("mergeinput").set(1)
n_rop_geo2.parm("externalpath").set("$HIP/geo/$HIPNAME.$OS.`@pdg_index`.`@wedgenum`.bgeo.sc")
n_rop_geo2.setInput(0, n_part_att)


# obj > topnet
n_rop_import2 = topnet.createNode("ropgeometry")
n_rop_import2.setName("build_streets")
n_rop_import2.parm("usesoppath").set(0)
n_rop_import2.parm("sopoutput").set("$HIP/geo/$HIPNAME.$OS.`@wedgenum`.bgeo.sc1")
n_rop_import2.parm("pdg_cachemode").set(2)
n_rop_import2.parm("pdg_cooktype").set(3)
n_rop_import2.setInput(0, n_hdaprocessor)

# obj > topnet > ropgeometryimport
n_rop2_in = hou.node(n_rop_import2.path()+'/s/s')
n_out = hou.node('/obj/topnet1/create_building/s/s/output1')
n_out.setInput(0, None)

n2_extrude1 = n_rop2_in.createNode("polyextrude::2.0")
n2_extrude1.parm("dist").set(-0.05)
n2_extrude1.parm("outputfront").set(0)
n2_extrude1.parm("outputback").set(1)
n2_extrude1.parm("outputside").set(1)
n2_extrude1.setInput(0,hou.node('/obj/topnet1/ropgeometry1/s/s/incoming'))

n2_reverse = n_rop2_in.createNode("reverse")
n2_reverse.setInput(0, n2_extrude1)

n2_color = n_rop2_in.createNode("color")
n2_color.setInput(0, n2_reverse)

n2_merge = n_rop2_in.createNode("merge")
n2_merge.setInput(0, n2_color)

n2_box = n_rop2_in.createNode("box")
n2_box.parm("type").set(1)
n2_box.parm("divrate1").set(2)
n2_box.parm("divrate2").set(2)
n2_box.parm("divrate3").set(2)
n2_box.setInput(0, n2_extrude1)

n2_blast = n_rop2_in.createNode("blast")
n2_blast.parm("group").set("2")
n2_blast.parm("negate").set(1)
n2_blast.setInput(0, n2_box)


n2_transform = n_rop2_in.createNode("xform")
n2_transform.parm("ty").set(-0.05)
n2_transform.parm("sx").set(1.05)
n2_transform.parm("sy").set(1)
n2_transform.parm("sz").set(1.05)
n2_transform.setInput(0, n2_blast)


n2_color2 = n_rop2_in.createNode("color")
n2_color2.parm("colorr").set(0.33)
n2_color2.parm("colorg").set(0.33)
n2_color2.parm("colorb").set(0.33)
n2_color2.setInput(0, n2_transform)

n2_merge.setInput(1, n2_color2)
n_out.setInput(0, n2_merge)


# obj > topnet > patitionbyindex
n_partition_idx = topnet.createNode("partitionbyindex")
n_partition_idx.setInput(0, n_rop_geo2)


###########################################################################################################
# n_work_viewer2 노드 안에 file 노드 생성 후 값 세팅
file_node = n_work_viewer2.createNode("file")
file_node.parm("file").set("`@pdg_output.1`")


##########################################################################################
# turntable setting

