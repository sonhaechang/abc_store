from typing import Any

from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest 

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from core.paginations import DefaultPagination

from shop.models import Item, Review, ReviewImage
from shop.serializers import ReviewSerializer



class ReviewAPIView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView):
	''' review 조회, 생성, 삭제하는 APIView '''

	pagination_class = DefaultPagination
	serializer_class = ReviewSerializer
	parser_classes = (MultiPartParser, FormParser, JSONParser,)
	item_model = Item
	review_model = Review

	def get_object(self) -> Model:
		''' 조건에 맞는 object을 반환 '''

		return get_object_or_404(self.item_model, pk=self.kwargs['item_pk'])

	def get_queryset(self) -> QuerySet[Any]:
		''' 조건에 맞는 queryset을 반환 '''

		return self.review_model.objects.filter(parent__isnull=True, item=self.get_object())
		
	def get_serializer_class(self) -> SerializerMetaclass:
		''' serializer_class를 반환 '''

		serializer = super().get_serializer_class()
		serializer.user = self.request.user
		return serializer

	def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		''' GET 요청을 처리하는 함수 '''

		serializer = self.list(request, *args, **kwargs)
		return serializer

	def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		''' POST 요청을 처리하는 함수 '''

		data = request.data
		parent_pk = data.get('parent_id')
		parent_obj = self.review_model.objects.get_or_none(pk=parent_pk)

		serializer = self.get_serializer(data=data)
		if serializer.is_valid(raise_exception=True):
			instance = serializer.save(
				user=request.user, 
				item=self.get_object())
			instance.parent = parent_obj
			instance.save()

			for image in request.FILES.getlist('images'):
				ReviewImage.objects.create(review=instance, image=image)

			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		else:
			print(serializer.errors)

	def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		''' DELETE 요청을 처리하는 함수 '''

		review_pk = request.data.get('review_id')
		review = self.review_model.objects.get_or_none(pk=review_pk)

		if review is None:
			return Response(status=status.HTTP_404_NOT_FOUND)

		if review.user != self.request.user:
			return Response(status=status.HTTP_403_FORBIDDEN)

		review.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)