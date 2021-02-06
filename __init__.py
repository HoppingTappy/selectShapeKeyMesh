import bpy
import bmesh

bl_info = {
	"name": "select shape key mesh",
	"author": "tappy",
	"version": (1, 0),
	"blender": (2, 91, 2),
	"location": "View3D > Edit > Select",
	"description": "シェイプキーで変形しているメッシュを選択するアドオン",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object",
}

translationDict = {
	"en_US": {
		("*", "Select Shape Key"):"Select Shape Key",
	},
	"ja_JP": {
		("*", "Select Shape Key"):"シェイプキー選択",
	}
}

class SELECT_OT_selectShapeKeyVertices(bpy.types.Operator):

	bl_idname = "object.select_shape_key_vertices"
	bl_label = bpy.app.translations.pgettext("Select Shape Key")
	bl_description = "シェイプキーで変形しているメッシュを選択します"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='DESELECT')

		obj=bpy.context.edit_object
		bMesh = bmesh.from_edit_mesh(obj.data)
		bMeshSel = bmesh.new()
		bMeshRel = bmesh.new()

		selectedShapeKey = obj.active_shape_key
		relativeShapeKey = selectedShapeKey.relative_key

		index = obj.data.shape_keys.key_blocks.keys().index(selectedShapeKey.name)
		bMeshSel.from_mesh(obj.data,use_shape_key=True, shape_key_index=index)
		index = obj.data.shape_keys.key_blocks.keys().index(relativeShapeKey.name)
		bMeshRel.from_mesh(obj.data,use_shape_key=True, shape_key_index=index)

		selectMode = bpy.context.tool_settings.mesh_select_mode[:]
		if selectMode == (True,False,False):
			for s,r,o in zip(selectedShapeKey.data, relativeShapeKey.data, bMesh.verts):
				if s.co != r.co:
					o.select = True
		elif selectMode == (True,True,False) or selectMode == (False,True,False):
			for s,r,o in zip(bMeshSel.edges, bMeshRel.edges, bMesh.edges):
				if s.verts[0].co != r.verts[0].co or s.verts[1].co != r.verts[1].co:
					o.select = True
		elif selectMode[2] == True:
			for s,r,o in zip(bMeshSel.faces, bMeshRel.faces, bMesh.faces):
				if s.calc_center_median() != r.calc_center_median():
					o.select = True

		bMesh.select_flush_mode()

		return {'FINISHED'}

def addMenu(self, context):
	self.layout.separator()
	self.layout.operator(SELECT_OT_selectShapeKeyVertices.bl_idname,text=bpy.app.translations.pgettext("Select Shape Key"))

classes = [
	SELECT_OT_selectShapeKeyVertices,
]

def register():
	bpy.app.translations.register(__name__, translationDict)
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_select_edit_mesh.append(addMenu)


def unregister():
	bpy.app.translations.unregister(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(addMenu)
	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register()
