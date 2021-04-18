from django.core.paginator import Paginator as DjangoPaginator


class Paginator():
    def __init__(self, queryset, request, page_size=10, param='page'):
        self.queryset = queryset
        self.request = request
        self.page_size = page_size
        self.param = param

    def get_page(self):
        paginator = DjangoPaginator(self.queryset, self.page_size)
        page_number = self.request.GET.get(self.param)
        page_obj = paginator.get_page(page_number)
        return page_obj
