class FilterMixin:
    """
    필터 믹스인

    from django_filters import FilterSet

    사용법:
    - FilterSet을 상속받은 필터 클래스를 "filter_class filter_class = FilterSet()" 사용
    - Tempalte에서 "{{ search_filter.form }}" 으로 필터 폼 사용

    """
    filter_class = None
    filter = None

    def get_filter_class(self):
        return self.filter_class if self.filter_class else None

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_class = self.get_filter_class()

        if filter_class:
            self.filter = filter_class(self.request.GET, queryset=queryset)
            queryset = self.filter.qs

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.filter:
            context['search_filter'] = self.filter
        return context


class UserAuditMixin:
    """ 사용자 정보를 저장하는 Mixin """

    user_fields: tuple = ('created_by', 'updated_by',)

    def get_user_fields(self) -> tuple:
        """ 사용자 정보를 저장할 필드명 반환 """
        return self.user_fields

    def form_valid(self, form):
        # self의 클래스 이름을 문자열로 확인
        class_name = type(self).__name__
        create_filed, update_field = self.get_user_fields()
        user = self.reqeust.user

        # CreateView와 UpdateView를 문자열로 확인
        if class_name == 'CreateView':
            if hasattr(form.instance, create_filed):
                setattr(form.instance, create_filed, user)
            if hasattr(form.instance, update_field):
                setattr(form.instance, update_field, user)
        elif class_name == 'UpdateView':
            if hasattr(form.instance, update_field):
                setattr(form.instance, update_field, user)

        return super().form_valid(form)


class PageTitleMixin:
    """ 페이지 타이틀 믹스인 """

    page_title: str = None

    def get_page_title(self):
        """ 페이지 타이틀 반환 """
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        return context
