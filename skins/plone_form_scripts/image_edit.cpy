## Controller Python Script "image_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=precondition='', file='', id='', title=None, description=None
##title=Edit an image
##

original_id=context.getId()
filename=getattr(file,'filename', '')

if file and filename and context.isIDAutoGenerated(original_id):
#  if there is no id or an autogenerated id, use the filename as the id
#  if not id or context.isIDAutoGenerated(id):
#  if there is no id, use the filename as the id
    if not id:
        id = filename[max( string.rfind(filename, '/')
                       , string.rfind(filename, '\\')
                       , string.rfind(filename, ':') )+1:]

file.seek(0)

# if there is no id specified, keep the current one
if not id:
    id = context.getId()

new_context = context.portal_factory.doCreate(context, id)

new_context.plone_utils.contentEdit(new_context,
                                    id=id,
                                    title=title,
                                    description=description)

new_context.edit( precondition=precondition, file=file )

from Products.CMFPlone import transaction_note
transaction_note('Edited image %s at %s' % (new_context.title_or_id(), new_context.absolute_url()))

return state.set(context=new_context,
                 portal_status_message='Image changes saved.')
