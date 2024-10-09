from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    自定义分页
    """
    page_query_param = 'page_num'  # url 中页码字段名
    page_size_query_param = 'page_size'  # 支持在 url 中控制分页大小
    page_size = 10  # 默认每页显示的记录数
    max_page_size = 20  # 客户端可以请求的最大记录数
