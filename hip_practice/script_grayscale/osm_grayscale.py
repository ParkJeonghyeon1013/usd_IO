import hou

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
n_work_viewer2.setName('WORK_Building_VIEWER2')

n_render_viewer1 = obj.node('geo4')
n_render_viewer1.setName('RENDER_Street_VIEWER1')

n_render_viewer2 = obj.node('geo5')
n_render_viewer2.setName('RENDER_Street_VIEWER2')

# topnet 작업 > wedge 노드 세팅
# def topnet_wedge():
topnet = obj.node('topnet1')
wedge = topnet.node('wedge1')
wedge.parm("wedgecount").set(4)
wedge.parm("wedgeattributes").set(3)


#################################################################################################################################################
# n_work_viewer1 노드 안에 file 노드 생성 후 값 세팅
# def n_work_viewer():
file_node = n_work_viewer1.createNode('file1')
file_node.parm("file").set("`@pdg_output`")

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

# houdini asset 만들기
# TODO: houdini asset 만들 때 HDA 저장 방식 픽스해주기!!!!
hou.Node.createDigitalAsset(n_subnet)

# null 생성해서 연결
n_street_grid.createNode("null")
null = n_street_grid.createNode("null")
null.setName("CITYBLOCKS_OUT")
null.setInput(0, n_subnet)



















########################################################################################################################################
# obj > topnet > localscheduler
n_localscheduler = topnet.node('localscheduler')
n_localscheduler.parm('maxprocsmenu').set(-1)


# obj > topnet > geometryimport
n_geometryimport = topnet.createNode('geometryimport')
n_geometryimport.setName("cityblocks")
n_geometryimport.parm("geometrysource").set(0)


# hdaProcessor 1 = make_cirygrid
# TODO : QA ) 얘는 나중에 grid 기준으로 city 생성되면 할 수 있음. citygrid_maker HDA 만든거 사용하기 위함인데,, 아직 경로 지정하는 방법을 모르겠음.
#
topnet.createNode("hdaprocessor")
n_hdaprocessor = topnet.node("hdaprocessor1")
n_hdaprocessor.setInput(0, wedge)
n_hdaprocessor.setName("make_citygrid")
n_hdaprocessor.parm("inputfile").set("$HIP/hda/streetgrid_maker.hdanc")
n_hdaprocessor.parm("operatortype").set("Sop/USER::streetgrid_maker::1.0")
n_hdaprocessor.parm("hdatype").set(1)
n_hdaprocessor.parm("outputfile1").set("$HIP/geo/$OS.`@pdg_name`.`@wedgenum`.0.bgeo.sc")
n_hdaprocessor.parm("outputtag1").set("file/geo")
n_hdaprocessor.parm("updateHDAParms").set(1)

#
n_attribute_create = topnet.createNode("attributecreate")




# n_work_viewer2


