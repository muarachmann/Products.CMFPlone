## Script (Python) "image_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=precondition='', field_file='', field_id='', title=None, description=None
##title=Edit an image
##

errors=context.validate_image_edit()
if errors:
    form=getattr( context, context.getTypeInfo().getActionById( 'edit' ) )
    return form()

filename=getattr(field_file,'filename', '')
if field_file and filename:
    id=filename[max( string.rfind(filename, '/')
                   , string.rfind(filename, '\\')
                   , string.rfind(filename, ':') )+1:]

if field_file and filename:
    field_file.seek(0)

context.edit(
     precondition=precondition,
     file=field_file)

context.plone_utils.contentEdit(context,
                                id=field_id,
                                description=description)

qst='portal_status_message=Image+changed.'

context.REQUEST.RESPONSE.redirect( '%s/%s?%s' % ( context.absolute_url()
                                                , context.getTypeInfo().getActionById( 'view' )
                                                , qst
                                                ) )
