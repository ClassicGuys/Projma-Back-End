from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .invite_link import encode, decode
from .models import *
from .serializers import *
from .permissions import *
from accounts.serializers import *
# Create your views here.

class WorkspaceViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceMemberSerializer

    @action(methods=['get'], detail=False)
    def type(self, request):
        types = WorkSpace.TYPE_CHOICES
        dic_types = {t[0]: t[1] for t in types}
        return Response(dic_types)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='join-to-workspace/(?P<invite_link>.+)')
    def join_to_workspace(self, request, invite_link):
        workspace = decode(invite_link)
        if workspace is None:
            return Response('Invalid invite link', status=status.HTTP_400_BAD_REQUEST)
        try:
            if request.user.profile in workspace.members.all():
                return Response('You are already a member of this workspace', status=status.HTTP_400_BAD_REQUEST)
            workspace.members.add(request.user.profile)
            return Response('You have been added to the workspace successfully', status=status.HTTP_200_OK)
        except:
            return Response('Adding user to workspace failed', status=status.HTTP_400_BAD_REQUEST)


class UserDashboardViewset(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = WorkSpaceMemberSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='create-workspace', serializer_class=WorkSpaceOwnerSerializer)
    def create_workspace(self, request):
        serializer = WorkSpaceOwnerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], serializer_class=BoardAdminSerializer)
    def myboards(self, request):
        serializer = BoardAdminSerializer(instance=list(request.user.profile.boards.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
    @action(detail=False, methods=['get'], serializer_class=BoardAdminSerializer, url_path='myadministrating-boards')
    def myadministrating_boards(self, request):
        serializer = BoardAdminSerializer(instance=list(request.user.profile.administrating_boards.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=WorkSpaceOwnerSerializer)
    def myworkspaces(self, request):
        serializer = WorkSpaceMemberSerializer(instance=list(request.user.profile.workspaces.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='myowning-workspaces', serializer_class=WorkSpaceOwnerSerializer)
    def myowning_workspaces(self, request):
        serializer = WorkSpaceOwnerSerializer(instance=list(request.user.profile.owning_workspaces.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkSpaceOwnerViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceOwnerSerializer
    permission_classes = [IsWorkSpaceOwner | IsAdminUser]

    @action(detail=True, methods=['get'], url_path='memberboards/(?P<memberid>\d+)', serializer_class=BoardAdminSerializer)
    def memberboards(self, request, pk, memberid):
        memberprofile = get_object_or_404(Profile, pk=memberid)
        serializer = BoardAdminSerializer(instance=memberprofile.boards.all().filter(workspace=pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='workspace-members', serializer_class=ProfileSerializer)
    def workspace_members(self, request, pk):
        serializer = ProfileSerializer(instance=self.get_object().members.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='workspace-boards', serializer_class=BoardAdminSerializer)
    def workspace_boards(self, request, pk):
        serializer = BoardAdminSerializer(instance=self.get_object().boards.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='edit-workspace')
    def edit_workspace(self, request, pk):
        workspace = self.get_object()
        serializer = WorkSpaceOwnerSerializer(instance=workspace, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='get-workspace')
    def get_workspace(self, request, pk):
        workspace = self.get_object()
        serializer = WorkSpaceOwnerSerializer(instance=workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='delete-workspace')
    def delete_workspace(self, request, pk):
        workspace = self.get_object()
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, permission_classes=[IsWorkSpaceOwner], url_path='invite-link') 
    def invite_link(self, request, pk):
        workspace = self.get_object()
        invite_link = encode(workspace)
        return Response(invite_link, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True, url_path='create-board', serializer_class=BoardAdminSerializer)
    def create_board(self, request, pk):
        ws = self.get_object()
        serializer = BoardAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=ws)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BoardAdminViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardAdminSerializer
    permission_classes = [IsBoardAdmin | IsAdminUser | IsWorkSpaceOwner]

    @action(detail=True, methods=['patch'], url_path='edit-board')
    def edit_board(self, request, pk):
        board = self.get_object()
        serializer = BoardAdminSerializer(instance=board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'], url_path='delete-board')
    def delete_board(self, request, pk):
        board = self.get_object()
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='get-board')
    def get_board(self, request, pk):
        board = self.get_object()
        serializer = BoardAdminSerializer(instance=board)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardMembershipViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [IsMemberOfBoard | IsAdminUser | IsBoardAdmin | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='get-board')
    def get_board(self, request, pk):
        board = self.get_object()
        serializer = BoardMemberSerializer(instance=board)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkSpaceMemberViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceMemberSerializer
    permission_classes = [IsWorkSpaceMember | IsAdminUser | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='workspace-boards', serializer_class=BoardMemberSerializer)
    def workspace_boards(self, request, pk):
        serializer = BoardMemberSerializer(instance=self.get_object().boards.all().filter(members__user=request.user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='workspace-starred-boards', serializer_class=BoardMemberSerializer)
    def workspace_boards(self, request, pk):
        ws = self.get_object()
        userstarredboards = request.user.profile.starred_boards.all().filter(workspace=ws)
        serializer = BoardMemberSerializer(instance=userstarredboards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [IsMemberOfBoard | IsAdminUser | IsBoardAdmin | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        board = self.get_object()
        serializer = BoardMemberSerializer(instance=board.members.all() | board.admins.all(), many=True, context={'board': pk})
        return Response(serializer.data, status=status.HTTP_200_OK)