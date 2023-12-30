
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from photo.models import Photo
import oss2


def home(request):
    photos = Photo.objects.all()
    paginator = Paginator(photos, 5)
    page_number = request.GET.get('page')
    paged_photos = paginator.get_page(page_number)
    context = {'photos': paged_photos}

    # 处理登入登出的POST请求
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # 登入
        if user is not None and user.is_superuser:
            login(request, user)
        # 登出
        isLogout = request.POST.get('isLogout')
        if isLogout == 'True':
            logout(request)
    return render(request, 'photo/list.html', context)


def oss_home(request):
    photos = ObjIterator(bucket)
    paginator = Paginator(photos, 6)
    page_number = request.GET.get('page')
    paged_photos = paginator.get_page(page_number)
    context = {'photos': paged_photos}

    return render(request, 'photo/oss_list.html', context)


def upload(request):
    if request.method == 'POST' and request.user.is_superuser:
        images = request.FILES.getlist('images')
        for i in images:
            photo = Photo(image=i)
            photo.save()
    return redirect('home')


auth = oss2.Auth('LTAI5tECF28Vc1ZvmiUEkEfA', '45U09ckiUJ1czXnMlq0EXsrOO0xRnl')
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'unclesam-test')


class ObjIterator(oss2.ObjectIteratorV2):
    # 初始化时立即抓取图片数据
    def __init__(self, bucket):
        super().__init__(bucket)
        self.fetch_with_retry()

    # 分页要求实现__len__
    def __len__(self):
        return len(self.entries)

    # 分页要求实现__getitem__
    def __getitem__(self, key):
        return self.entries[key]

    # 此方法从云端抓取文件数据
    # 然后将数据赋值给 self.entries
    def _fetch(self):
        result = self.bucket.list_objects_v2(prefix=self.prefix,
                                             delimiter=self.delimiter,
                                             continuation_token=self.next_marker,
                                             start_after=self.start_after,
                                             fetch_owner=self.fetch_owner,
                                             encoding_type=self.encoding_type,
                                             max_keys=self.max_keys,
                                             headers=self.headers)
        self.entries = result.object_list + [oss2.models.SimplifiedObjectInfo(prefix, None, None, None, None, None)
                                             for prefix in result.prefix_list]
        # 让图片以上传时间倒序
        self.entries.sort(key=lambda obj: -obj.last_modified)

        return result.is_truncated, result.next_continuation_token

# Create your views here.
