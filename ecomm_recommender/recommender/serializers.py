from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Product, Rating, UserInteraction, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["hobby", "interest"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="userprofile", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    hobby = serializers.CharField(required=False, allow_blank=True)
    interest = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "hobby", "interest"]

    def create(self, validated_data):
        hobby = validated_data.pop("hobby", "")
        interest = validated_data.pop("interest", "")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )

        # create linked UserProfile
        UserProfile.objects.create(
            user=user,
            hobby=hobby,
            interest=interest
        )

        return user


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"  # all product fields + extra
        extra_fields = ["avg_rating", "rating_count"]

    def get_avg_rating(self, obj):
        avg = obj.rating_set.aggregate(avg=Avg("rating"))["avg"]

        return round(avg, 1) if avg else 0.0

    def get_rating_count(self, obj):
        return obj.rating_set.count()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = "__all__"

