from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    role = models.SmallIntegerField(verbose_name="角色")

    class Meta:
        db_table = "tb_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Project(BaseModel):
    name = models.CharField(max_length=20, unique=True, verbose_name="项目名称")
    owner = models.ForeignKey("User", related_name="projects", blank=True, on_delete=models.SET_NULL,null=True,
                              verbose_name="项目管理者")

    class Meta:
        db_table = "projects"
        verbose_name = "项目表"


class Category(BaseModel):
    name = models.CharField(max_length=20, unique=True, verbose_name="分类名称")
    project = models.ForeignKey("Project", related_name="categorys", blank=True, on_delete=models.SET_NULL,null=True,
                                verbose_name="所属项目")
    category_owner = models.ForeignKey("User", related_name="categorys", blank=True, on_delete=models.SET_NULL,null=True,
                              verbose_name="单类文书管理者")

    class Meta:
        db_table = "categories"
        verbose_name = "类别表"


class UserRelation(BaseModel):
    parent = models.ForeignKey("User", related_name="parents", blank=True, on_delete=models.CASCADE,
                               verbose_name="打标签者_上级")
    sub = models.ForeignKey("User", related_name="subs", blank=True, on_delete=models.CASCADE, verbose_name="打标签_下级")
    category = models.ForeignKey("Category", related_name="categories", blank=True, on_delete=models.CASCADE,
                                 verbose_name="所在类别")

    class Meta:
        db_table = "userrelations"
        verbose_name = "用户关系表"

class Document(BaseModel):
    text = models.TextField(verbose_name="文书内容")
    category = models.ForeignKey("Category", related_name="documents", blank=True, on_delete=models.SET_NULL,null=True,
                                 verbose_name="所属类别")
    annotated_by = models.ForeignKey("User", related_name="documents", blank=True, on_delete=models.SET_NULL,null=True,
                                     verbose_name="打标签者")

    class Meta:
        db_table = "documents"
        verbose_name = "文书表"

    def __str__(self):
        return self.text[:50]


class Annotation(BaseModel):
    document = models.ForeignKey("Document", related_name="annotations", blank=True, on_delete=models.CASCADE,
                                verbose_name="所属文本")
    # 概率
    prob = models.FloatField(default=0.0)
    # 是否人工标注
    manual = models.BooleanField(default=False)
    # 所用标记
    label = models.ForeignKey("Label", related_name="annotations", blank=True, on_delete=models.SET_NULL,null=True,
                              verbose_name="标记")
    # 文档中的开始位置
    start_offset = models.IntegerField(verbose_name="标记开始下标")
    # 文档中的结束位置
    end_offset = models.IntegerField()

    class Meta:
        db_table = "annotations"
        verbose_name = "标签表"


class Label(BaseModel):
    text = models.CharField(max_length=100)
    background_color = models.CharField(max_length=7, default='#209cee')
    text_color = models.CharField(max_length=7, default='#ffffff')

    class Meta:
        db_table = "labels"
        verbose_name = "标记表"
