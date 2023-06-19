# Get box size
gizmo = nuke.thisNode()
gizmoName = gizmo.knob('name').getValue()
inputNode = gizmo.input(0)
boxWidth = inputNode.format().width()
boxHeight = inputNode.format().height()

# Go inside Gizmo
gizmo.begin()

# Delete previously created nodes
createdTransformNodes = nuke.allNodes('Transform')
for node in createdTransformNodes:
    if 'TransformX' in node['name'].value() or 'TransformY' in node['name'].value():
        nuke.delete(node)
createdMergeNodes = nuke.allNodes('Merge')
for node in createdMergeNodes:
    nuke.delete(node)
try:
    nuke.delete(nuke.toNode('Reformat1'))
except:
    pass

# Get inputs from properties tab
reformatBool = bool(gizmo.knob('resize_box').getValue())
repeatX = int(gizmo.knob('repeatX').getValue())
repeatY = int(gizmo.knob('repeatY').getValue())

# Create X repetitions
for x in range(1, repeatX + 1):
    TransformXx = 'TransformX' + str(x)
    TransformX0 = 'TransformX' + str(x-1)
    MergeXx = 'MergeX' + str(x)
    MergeX0 = 'MergeX' + str(x-1)
    nodeTransformX0 = nuke.toNode(TransformX0)
    nodeMergeX0 = nuke.toNode(MergeX0)
    nuke.nodes.Transform(name = TransformXx, inputs = [nodeTransformX0], translate = str('-' + gizmoName + '.blur_edges+' + str(boxWidth) + ' 0'))
    nodeTransformXx = nuke.toNode(TransformXx)
    nuke.nodes.Merge(name = MergeXx, inputs = [nodeMergeX0, nodeTransformXx], operation = 'under')
    nodeMergeXx = nuke.toNode(MergeXx)

# Create Y repetitions
for y in range(1, repeatY + 1):
    TransformYy = 'TransformY' + str(y)
    TransformY0 = 'TransformY' + str(y-1)
    MergeYy = 'MergeY' + str(y)
    MergeY0 = 'MergeY' + str(y-1)
    nodeTransformY0 = nuke.toNode(TransformY0)
    nodeMergeY0 = nuke.toNode(MergeY0)
    nuke.nodes.Transform(name = TransformYy, inputs = [nodeTransformY0], translate = str('0 -' + gizmoName + '.blur_edges+' + str(boxHeight)))
    nodeTransformYy = nuke.toNode(TransformYy)
    nuke.nodes.Merge(name = MergeYy, inputs = [nodeMergeY0, nodeTransformYy], operation = 'under')
    nodeMergeYy = nuke.toNode(MergeYy)

# Connect repetitions to tree
outputX = nuke.toNode('OutputX')
outputY = nuke.toNode('OutputY')
lastMergeX = nuke.toNode(str('MergeX' + str(repeatX)))
outputX.setInput(0, lastMergeX)
lastMergeY = nuke.toNode(str('MergeY' + str(repeatY)))
outputY.setInput(0, lastMergeY)

# Adjust box size
if reformatBool:
    Reformat1 = nuke.nodes.Reformat(inputs = [outputY], type = 'to box', box_width = str('-' + gizmoName + '.blur_edges*' + str(repeatX+1) + '+' + str(boxWidth*(repeatX+1))), box_height = str('-' + gizmoName + '.blur_edges*' + str(repeatY+1) + '+' + str(boxHeight*(repeatY+1))), resize = 'none', center = 0)
    output = nuke.toNode('Output1')
    output.setInput(0, Reformat1)