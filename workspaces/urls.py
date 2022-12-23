from rest_framework.routers import DefaultRouter
from .views import board, workspace, tasklist, label, task, checklist, templates, comment


router = DefaultRouter()

router.register('workspaces', workspace.WorkspaceViewSet, basename='workspaces')
router.register('workspaces', workspace.WorkSpaceStarredBoardsViewSet, basename='workspaces')
router.register('workspaceowner', workspace.WorkSpaceOwnerViewSet, basename='workspaceowner')
router.register('workspacemember', workspace.WorkSpaceMemberViewSet, basename='workspacemember')
router.register('dashboard', workspace.UserDashboardViewset, basename='dashboard')
router.register('board/(?P<b_id>[^/.]+)/members', board.BoardMembersViewSet, basename='board')
router.register('board/(?P<b_id>[^/.]+)', board.BoardRoleViewSet, basename='board')
router.register('board', board.BoardInviteLinkViewSet, basename='board')
router.register('board', board.RemoveOrJoinToBoardViewSet, basename='board')
router.register('board', label.CreateLabelViewSet, basename='board')
router.register('board', board.GetBoardLabelsViewSet, basename='board')
router.register('board', tasklist.CreateTaskListViewSet, basename='board')
router.register('board', board.GetBoardTaskListsViewSet, basename='board')
router.register('board', board.GetBoardOverviewViewSet, basename='board')
router.register('board', board.ToggleBoardStarViewSet, basename='board')
router.register('board', tasklist.ReorderTaskListsViewSet, basename='board')
router.register('tasklist', task.CreateTaskViewSet, basename='tasklist')
router.register('boardsadminapi', board.BoardAdminViewSet, basename='boardsadminapi')
router.register('boardsmemberapi', board.BoardMembershipViewSet, basename='boardsmemberapi')
router.register('label', label.UpdateLabelViewSet, basename='board')
router.register('label', label.DeleteLabelViewSet, basename='board')
router.register('tasklist', tasklist.UpdateTaskListViewSet, basename='board')
router.register('tasklist', tasklist.DeleteTaskListViewSet, basename='board')
router.register('tasklist', task.ReorderTaskListsViewSet, basename='board')
router.register('task/(?P<b_id>[^/.]+)', task.FilterBoardViewSet, basename='board')
router.register('task', task.UpdateTaskViewSet, basename='task')
router.register('task', task.MoveTaskViewSet, basename='task')
router.register('task', task.AddLabelsToTaskViewSet, basename='task')
router.register('task', task.DeleteLabelsFromTaskViewSet, basename='task')
router.register('task', task.AddDoersToTaskViewSet, basename='task')
router.register('task', task.DeleteDoersFromTaskViewSet, basename='task')
router.register('task', task.GetTaskViewSet, basename='task')
router.register('task', task.GetTaskPreviewViewSet, basename='task')
router.register('task', task.DeleteTaskViewSet, basename='task')
router.register('task', checklist.CreateOrReadCheckListViewSet, basename='checklist')
router.register('task/update-checklist', checklist.UpdateCheckListViewSet, basename='checklist')
router.register('task/delete-checklist', checklist.DeleteCheckListViewSet, basename='checklist')
router.register('task', comment.NewCommentViewset, basename='task')
router.register('comment', comment.ReplyCommentViewSet, basename='comment')
router.register('comment', comment.EditCommentViewSet, basename='comment')
router.register('comment', comment.DeleteCommentViewSet, basename='comment')
router.register('task', task.AddAttachmentToTaskViewSet, basename='task')
router.register('attachment', task.DeleteAttachmentFromTaskViewSet, basename='attachment')
router.register('templates', templates.TemplateViewSet, basename='templates')


urlpatterns = router.urls