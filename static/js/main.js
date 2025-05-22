$(document).ready(function() {
    // Автоматическое скрытие уведомлений
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Обработка формы комментария
    $('textarea[name="content"]').on('focus', function() {
        $(this).attr('rows', 3);
        $(this).parent().siblings('.comment-actions').show();
    });

    $('.cancel-comment').on('click', function() {
        const textarea = $(this).parent().siblings('.form-group').find('textarea');
        textarea.attr('rows', 1);
        textarea.val('');
        $(this).parent().hide();
    });

    // Отправка комментария через AJAX
    $('#commentForm').on('submit', function(e) {
        e.preventDefault();

        const form = $(this);
        const formData = new FormData(form[0]);

        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                // Добавляем новый комментарий в начало списка
                const newComment = `
                    <div class="comment mb-3 fade-in" id="comment-${data.id}">
                        <div class="d-flex">
                            <img src="${$('#commentForm img').attr('src')}" alt="${data.author}" class="rounded-circle mr-3" width="40" height="40">
                            <div class="flex-grow-1">
                                <div class="d-flex align-items-center mb-1">
                                    <span class="font-weight-bold mr-2">${data.author}</span>
                                    <small class="text-muted">только что</small>
                                </div>
                                <p class="mb-2">${data.content}</p>
                                <div class="comment-actions">
                                    <button class="btn btn-sm btn-link like-comment" data-id="${data.id}">
                                        <i class="fas fa-thumbs-up"></i> <span class="like-count">${data.likes}</span>
                                    </button>
                                    <button class="btn btn-sm btn-link dislike-comment" data-id="${data.id}">
                                        <i class="fas fa-thumbs-down"></i> <span class="dislike-count">${data.dislikes}</span>
                                    </button>
                                    <button class="btn btn-sm btn-link reply-btn" data-id="${data.id}">Ответить</button>
                                    <button class="btn btn-sm btn-link text-danger delete-comment" data-id="${data.id}">Удалить</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                $('#comments-list').prepend(newComment);

                // Очищаем форму
                form.find('textarea').val('').attr('rows', 1);
                form.find('.comment-actions').hide();

                // Обновляем счетчик комментариев
                const commentsCount = $('.comments-section h4');
                const currentCount = parseInt(commentsCount.text().split(' ')[0]);
                commentsCount.text((currentCount + 1) + ' комментариев');
            },
            error: function(xhr, status, error) {
                console.log('Ошибка при отправке комментария:', error);
                alert('Произошла ошибка при отправке комментария. Попробуйте еще раз.');
            }
        });
    });

    // Показать/скрыть форму ответа
    $(document).on('click', '.reply-btn', function() {
        const commentId = $(this).data('id');
        const replyForm = $('#reply-form-' + commentId);

        if (replyForm.is(':visible')) {
            replyForm.hide();
        } else {
            // Скрываем все остальные формы ответов
            $('.reply-form').hide();
            replyForm.show();
            replyForm.find('textarea').focus();
        }
    });

    // Отмена ответа
    $(document).on('click', '.cancel-reply', function() {
        const replyForm = $(this).closest('.reply-form');
        replyForm.hide();
        replyForm.find('textarea').val('');
    });

    // Плавная прокрутка к комментариям
    $('.scroll-to-comments').on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $('.comments-section').offset().top - 80
        }, 500);
    });

    // Lazy loading для изображений
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // Поиск с автодополнением
    let searchTimeout;
    $('#searchInput').on('input', function() {
        const query = $(this).val();

        clearTimeout(searchTimeout);

        if (query.length > 2) {
            searchTimeout = setTimeout(function() {
                // Здесь можно добавить AJAX запрос для автодополнения
                console.log('Поиск:', query);
            }, 300);
        }
    });

    // Автоматическое изменение размера textarea
    $('textarea').on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Подтверждение удаления
    $('.delete-confirm').on('click', function(e) {
        if (!confirm('Вы уверены, что хотите удалить это?')) {
            e.preventDefault();
        }
    });

    // Копирование ссылки на видео
    $('.copy-link').on('click', function() {
        const url = window.location.href;

        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(function() {
                showNotification('Ссылка скопирована!', 'success');
            });
        } else {
            // Fallback для старых браузеров
            const textArea = document.createElement('textarea');
            textArea.value = url;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Ссылка скопирована!', 'success');
        }
    });

    // Функция для показа уведомлений
    function showNotification(message, type) {
        const notification = $(`
            <div class="alert alert-${type} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `);

        $('body').append(notification);

        setTimeout(function() {
            notification.fadeOut(function() {
                $(this).remove();
            });
        }, 3000);
    }

    // Загрузка видео с предпросмотром
    $('#id_file').on('change', function() {
        const file = this.files[0];

        if (file) {
            const video = document.createElement('video');
            video.preload = 'metadata';

            video.onloadedmetadata = function() {
                window.URL.revokeObjectURL(video.src);

                // Создаем canvas для создания миниатюры
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                canvas.width = 320;
                canvas.height = 180;

                video.currentTime = Math.min(video.duration / 2, 5); // Берем кадр из середины или через 5 сек

                video.onseeked = function() {
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                    canvas.toBlob(function(blob) {
                        const thumbnailFile = new File([blob], 'thumbnail.jpg', {
                            type: 'image/jpeg'
                        });

                        // Можно автоматически установить миниатюру
                        console.log('Создана миниатюра:', thumbnailFile);
                    }, 'image/jpeg', 0.8);
                };
            };

            video.src = URL.createObjectURL(file);
        }
    });
});

// Функция для форматирования времени
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

// Функция для форматирования количества просмотров
function formatViews(count) {
    if (count >= 1000000) {
        return (count / 1000000).toFixed(1) + 'М';
    } else if (count >= 1000) {
        return (count / 1000).toFixed(1) + 'К';
    }
    return count.toString();
}
