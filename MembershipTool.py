from Products.CMFDefault.MembershipTool import MembershipTool
from Products.CMFDefault import Document
from Products.CMFCore.utils import getToolByName
import PloneFolder 

default_member_content = '''Default page for %s

  This is the default document created for you when 
  you joined this community.

  To change the content just select "Edit"
  in the tabs along the top of this form.
'''

class MembershipTool(MembershipTool):
    """ Plone customized Membership Tool """
    meta_type='Plone Membership Tool'
    plone_tool = 1

    def createMemberarea(self, member_id):
        """
        create a member area with a workflow enabled homepage
        """
        parent=self.aq_inner.aq_parent
        members=getattr(parent, 'Members', None)
    
        if members is not None and not hasattr(members, member_id):
            f_title = "%s's Home" % member_id
            #addPloneFolder(members, id=member_id )
            if members.meta_type=='Plone Folder':
                members.manage_addPloneFolder( member_id, f_title )
            else:
                members.manage_addPortalFolder( member_id, f_title)

            f=getattr(members, member_id)
    
            # Grant ownership to Member
            acl_users = self.__getPUS()
            user = acl_users.getUser(member_id).__of__(acl_users)
            f.changeOwnership(user)
            f.manage_setLocalRoles(member_id, ['Owner'])
    
            # Create Member's home page.
            # default_member_content ought to be configurable per
            # instance of MembershipTool.
    
            # the below skips workflow                          
            Document.addDocument( f
                                , 'index_html'
                                , member_id+"'s Home"
                                , member_id+"'s front page"
                                , "structured-text"
                                , (default_member_content % member_id)
                                )
    
            wf_tool=getToolByName(self, 'portal_workflow')
            homepage=getattr(f, 'index_html')
            wf = wf_tool.getWorkflowsFor(homepage)[0]
            wf.updateRoleMappingsFor(homepage)
    
            f.index_html._setPortalTypeName( 'Document' )
            # Overcome an apparent catalog bug.
            f.index_html.reindexObject()

            #Add .personal folder for Portraits and Personal content
            if f.meta_type=='Plone Folder':
                f.manage_addPloneFolder(id='.personal', title='Personal Items' )
            else:
                f.manage_addPortalFolder(id='.personal', title='Personal Items')
