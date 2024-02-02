from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import UsefulHabit
from main.serializers import UsefulHabitSerializer
from main.permissions import IsOwner
from main.paginators import MainPaginator


class UsefulHabitCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer


class UsefulHabitListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer
    pagination_class = MainPaginator

    def get_queryset(self):
        return UsefulHabit.objects.filter(owner=self.request.user)


class UsefulHabitViewAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()


class UsefulHabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()


class UsefulHabitDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()


class UsefulHabitPublicListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer

    def get_queryset(self):
        return UsefulHabit.objects.filter(is_public=True)
