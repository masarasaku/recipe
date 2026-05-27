from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from .models import Book
from .forms import BookForm


def book_list(request):
    
    books = Book.objects.all()
    
    return render(request, 'bookapp/book_list.html',{'book_list' : books})
def book_detail(request, pk):
    target = get_object_or_404(Book, pk=pk)
    return render(request, 'bookapp/book_detail.html', {'book': target})
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '書籍が正常に登録されました。')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookapp/book_form.html', {'form': form, 'title': '書籍登録'})
def book_update(request, pk):
    target = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            messages.success(request, '書籍が正常に更新されました。')
            return redirect('book_list')
    else:
        form = BookForm(instance=target)
    return render(request, 'bookapp/book_form.html', {'form': form, 'title': '書籍編集'})
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, '書籍が正常に削除されました。')
        return redirect('book_list')
    return render(request, 'bookapp/book_confirm_delete.html', {'book': book})
def add_messages(request):
    messages.success(request, 'これは成功メッセージです。')
    messages.error(request, 'これはエラーメッセージです。')
    messages.info(request, 'これは情報メッセージです。')
    messages.warning(request, 'これは警告メッセージです。')
    messages.debug(request, 'これはデバッグメッセージです。')
    return redirect('display_messages')
def show_display_messages(request):
    return render(request, 'bookapp/show_all_messages.html')
# Create your views here.
