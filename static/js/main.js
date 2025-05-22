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
// Глобальные переменные
let notificationUpdateInterval;
let recommendationEngine;

$(document).ready(function() {
    // Инициализация
    initializeApp();

    // Автообновление уведомлений
    startNotificationUpdates();

    // Инициализация системы рекомендаций
    initializeRecommendations();

    // Обработчики событий
    setupEventHandlers();
});

function initializeApp() {
    // Автоматическое скрытие уведомлений
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Инициализация tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Lazy loading для изображений
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

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

function startNotificationUpdates() {
    // Обновляем счетчик уведомлений каждые 30 секунд
    notificationUpdateInterval = setInterval(function() {
        updateNotificationCount();
    }, 30000);
}

function updateNotificationCount() {
    $.get('/notifications/api/unread-count/').done(function(data) {
        const badge = $('#notificationCount');
        if (data.count > 0) {
            badge.text(data.count).show();
        } else {
            badge.hide();
        }
    });
}

function initializeRecommendations() {
    // Загружаем рекомендации при скролле до конца страницы
    let loading = false;

    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
            if (!loading && $('#loadMoreRecommendations').length) {
                loading = true;
                loadMoreRecommendations();
            }
        }
    });
}

function loadMoreRecommendations() {
    const page = parseInt($('#loadMoreRecommendations').data('page')) || 1;

    $.get(`/api/recommendations/?page=${page + 1}`).done(function(data) {
        if (data.videos.length > 0) {
            let html = '';
            data.videos.forEach(function(video) {
                html += createVideoCard(video);
            });

            $('#videoGrid').append(html);
            $('#loadMoreRecommendations').data('page', page + 1);

            // Lazy loading для новых изображений
            initializeLazyLoading();
        } else {
            $('#loadMoreRecommendations').hide();
        }
    }).always(function() {
        loading = false;
    });
}

function createVideoCard(video) {
    return `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4 fade-in">
            <div class="card video-card h-100">
                <div class="video-thumbnail position-relative">
                    <a href="/video/${video.id}/">
                        <img src="${video.thumbnail}" class="card-img-top" alt="${video.title}">
                        <span class="video-duration">${video.duration}</span>
                    </a>
                </div>
                <div class="card-body">
                    <h6 class="card-title">
                        <a href="/video/${video.id}/" class="text-decoration-none">${video.title}</a>
                    </h6>
                    <div class="d-flex align-items-center mb-2">
                        <img src="${video.uploader.avatar}" class="rounded-circle me-2" width="24" height="24">
                        <a href="/user/${video.uploader.username}/" class="text-muted text-decoration-none small">
                            ${video.uploader.username}
                        </a>
                    </div>
                    <div class="text-muted small">
                        ${formatViews(video.views)} просмотров • ${video.created_ago}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function setupEventHandlers() {
    // Добавление в плейлист
    $(document).on('click', '.add-to-playlist-btn', function() {
        const videoId = $(this).data('video-id');
        showPlaylistModal(videoId);
    });

    // Поиск с автодополнением
    let searchTimeout;
    $('#searchInput').on('input', function() {
        const query = $(this).val();

        clearTimeout(searchTimeout);

        if (query.length > 2) {
            searchTimeout = setTimeout(function() {
                showSearchSuggestions(query);
            }, 300);
        } else {
            hideSearchSuggestions();
        }
    });

    // Отслеживание времени просмотра видео
    if ($('video').length) {
        trackVideoWatching();
    }

    // Бесконечная прокрутка комментариев
    setupInfiniteCommentScroll();
}

function showPlaylistModal(videoId) {
    // Загружаем плейлисты пользователя
    $.get(`/playlists/get-playlists/${videoId}/`).done(function(data) {
        let html = '';
        data.playlists.forEach(function(playlist) {
            const checked = playlist.is_in_playlist ? 'checked' : '';
            html += `
                <div class="form-check">
                    <input class="form-check-input playlist-checkbox" type="checkbox" 
                           value="${playlist.id}" ${checked} data-video-id="${videoId}">
                    <label class="form-check-label">
                        ${playlist.title} (${playlist.video_count} видео)
                    </label>
                </div>
            `;
        });

        $('#playlistOptions').html(html);
        $('#playlistModal').modal('show');
    });
}

function showSearchSuggestions(query) {
    $.get(`/api/search-suggestions/?q=${encodeURIComponent(query)}`).done(function(data) {
        let html = '';
        data.suggestions.forEach(function(suggestion) {
            html += `
                <div class="dropdown-item search-suggestion" data-query="${suggestion.text}">
                    <i class="fas fa-search me-2"></i>${suggestion.text}
                </div>
            `;
        });

        $('#searchSuggestions').html(html).show();
    });
}

function hideSearchSuggestions() {
    $('#searchSuggestions').hide();
}

function trackVideoWatching() {
    const video = $('video')[0];
    const videoId = $('#videoPlayer').data('video-id');
    let lastUpdateTime = 0;

    if (!video || !videoId) return;

    // Добавляем в историю при начале просмотра
    $.post(`/api/add-to-history/${videoId}/`, {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
    });

    // Обновляем продолжительность просмотра каждые 10 секунд
    setInterval(function() {
        if (!video.paused && video.currentTime > lastUpdateTime + 10) {
            lastUpdateTime = video.currentTime;

            $.post(`/api/update-watch-duration/${videoId}/`, {
                'duration': Math.floor(video.currentTime),
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            });
        }
    }, 10000);
}

function setupInfiniteCommentScroll() {
    let loading = false;
    const commentsContainer = $('#commentsContainer');

    if (!commentsContainer.length) return;

    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() > $(document).height() - 200) {
            if (!loading) {
                loading = true;
                loadMoreComments();
            }
        }
    });

    function loadMoreComments() {
        const videoId = $('#videoPlayer').data('video-id');
        const page = parseInt($('#loadMoreComments').data('page')) || 1;

        $.get(`/api/comments/${videoId}/?page=${page + 1}`).done(function(data) {
            if (data.comments.length > 0) {
                let html = '';
                data.comments.forEach(function(comment) {
                    html += createCommentHTML(comment);
                });

                $('#commentsList').append(html);
                $('#loadMoreComments').data('page', page + 1);
            } else {
                $('#loadMoreComments').hide();
            }
        }).always(function() {
            loading = false;
        });
    }
}

function createCommentHTML(comment) {
    return `
        <div class="comment-item" id="comment-${comment.id}">
            <div class="d-flex">
                <img src="${comment.author.avatar}" class="rounded-circle me-3" width="40" height="40">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-1">
                        <strong class="me-2">${comment.author.username}</strong>
                        <small class="text-muted">${comment.created_ago}</small>
                    </div>
                    <p class="mb-2">${comment.content}</p>
                    <div class="comment-actions">
                        <button class="btn btn-sm like-comment" data-id="${comment.id}">
                            <i class="fas fa-thumbs-up"></i> ${comment.likes}
                        </button>
                        <button class="btn btn-sm dislike-comment" data-id="${comment.id}">
                            <i class="fas fa-thumbs-down"></i> ${comment.dislikes}
                        </button>
                        <button class="btn btn-sm reply-comment" data-id="${comment.id}">
                            Ответить
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Плейлисты
$(document).on('change', '.playlist-checkbox', function() {
    const playlistId = $(this).val();
    const videoId = $(this).data('video-id');
    const isChecked = $(this).is(':checked');

    if (isChecked) {
        addToPlaylist(videoId, playlistId);
    } else {
        removeFromPlaylist(videoId, playlistId);
    }
});

function addToPlaylist(videoId, playlistId) {
    $.ajax({
        url: '/playlists/add-to-playlist/',
        method: 'POST',
        data: JSON.stringify({
            video_id: videoId,
            playlist_id: playlistId
        }),
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
        }
    }).done(function(response) {
        if (response.success) {
            showNotification('Видео добавлено в плейлист', 'success');
        } else {
            showNotification(response.message, 'error');
        }
    });
}

function removeFromPlaylist(videoId, playlistId) {
    $.ajax({
        url: `/playlists/${playlistId}/remove/${videoId}/`,
        method: 'POST',
        headers: {
            'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
        }
    }).done(function() {
        showNotification('Видео удалено из плейлиста', 'success');
    });
}

// Drag & Drop для плейлистов
function initializePlaylistSorting() {
    if (typeof Sortable !== 'undefined' && document.getElementById('playlistVideos')) {
        const sortable = Sortable.create(document.getElementById('playlistVideos'), {
            handle: '.drag-handle',
            animation: 150,
            onEnd: function(evt) {
                const playlistId = $('#playlistVideos').data('playlist-id');
                const videoOrders = [];

                $('#playlistVideos .playlist-video-item').each(function(index) {
                    videoOrders.push({
                        video_id: $(this).data('video-id'),
                        order: index + 1
                    });
                });

                $.ajax({
                    url: `/playlists/${playlistId}/reorder/`,
                    method: 'POST',
                    data: JSON.stringify({
                        video_orders: videoOrders
                    }),
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
                    }
                }).done(function(response) {
                    if (response.success) {
                        showNotification('Порядок видео обновлен', 'success');
                    }
                });
            }
        });
    }
}

// Уведомления в реальном времени (WebSocket)
function initializeWebSocket() {
    if ('WebSocket' in window) {
        const userId = $('body').data('user-id');
        if (!userId) return;

        const ws = new WebSocket(`ws://localhost:8000/ws/notifications/${userId}/`);

        ws.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type === 'notification') {
                showRealtimeNotification(data.notification);
                updateNotificationCount();
            }
        };

        ws.onclose = function(e) {
            console.log('WebSocket connection closed');
            // Попытка переподключения через 5 секунд
            setTimeout(function() {
                initializeWebSocket();
            }, 5000);
        };
    }
}

function showRealtimeNotification(notification) {
    // Показываем toast уведомление
    const toast = `
        <div class="toast position-fixed top-0 end-0 m-3" role="alert" style="z-index: 9999;">
            <div class="toast-header">
                <img src="${notification.sender_avatar}" class="rounded me-2" width="20" height="20">
                <strong class="me-auto">${notification.sender_name}</strong>
                <small class="text-muted">только что</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${notification.message}
            </div>
        </div>
    `;

    $('body').append(toast);
    $('.toast').toast('show');

    // Удаляем toast после скрытия
    $('.toast').on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

// Система рейтингов и рекомендаций
function updateVideoRating(videoId, action) {
    $.ajax({
        url: `/api/video/${videoId}/${action}/`,
        method: 'POST',
        headers: {
            'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
        }
    }).done(function(response) {
        if (response.success) {
            $('#likeCount').text(response.likes);
            $('#dislikeCount').text(response.dislikes);

            // Обновляем внешний вид кнопок
            if (action === 'like') {
                $('#likeBtn').toggleClass('btn-primary btn-outline-primary');
                $('#dislikeBtn').removeClass('btn-danger').addClass('btn-outline-danger');
            } else {
                $('#dislikeBtn').toggleClass('btn-danger btn-outline-danger');
                $('#likeBtn').removeClass('btn-primary').addClass('btn-outline-primary');
            }

            // Обновляем рекомендации на основе нового действия
            updateRecommendations();
        }
    });
}

function updateRecommendations() {
    // Обновляем рекомендации в фоне
    $.get('/api/update-recommendations/').done(function() {
        console.log('Рекомендации обновлены');
    });
}

// Полнотекстовый поиск
function performAdvancedSearch(filters) {
    const params = new URLSearchParams(filters);

    $.get(`/api/advanced-search/?${params.toString()}`).done(function(data) {
        updateSearchResults(data.videos);
        updateSearchFilters(data.filters);
    });
}

function updateSearchResults(videos) {
    let html = '';
    videos.forEach(function(video) {
        html += createVideoCard(video);
    });

    $('#searchResults').html(html);
    initializeLazyLoading();
}

// Аналитика просмотров
function trackVideoEvent(eventType, videoId, data = {}) {
    $.post('/api/analytics/track/', {
        'event_type': eventType,
        'video_id': videoId,
        'data': JSON.stringify(data),
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
    });
}

// Утилиты
function formatViews(count) {
    if (count >= 1000000) {
        return (count / 1000000).toFixed(1) + 'М';
    } else if (count >= 1000) {
        return (count / 1000).toFixed(1) + 'К';
    }
    return count.toString();
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'danger' : type;
    const toast = `
        <div class="toast position-fixed top-0 end-0 m-3" role="alert" style="z-index: 9999;">
            <div class="toast-header bg-${alertClass} text-white">
                <strong class="me-auto">Уведомление</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    $('body').append(toast);
    $('.toast').toast('show');

    $('.toast').on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

function initializeLazyLoading() {
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

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializePlaylistSorting();
    initializeWebSocket();

    // Отслеживание событий видео
    const video = document.querySelector('video');
    if (video) {
        const videoId = video.dataset.videoId;

        video.addEventListener('play', () => {
            trackVideoEvent('play', videoId);
        });

        video.addEventListener('pause', () => {
            trackVideoEvent('pause', videoId, {
                currentTime: video.currentTime
            });
        });

        video.addEventListener('ended', () => {
            trackVideoEvent('complete', videoId);
        });

        // Отслеживание прогресса просмотра
        video.addEventListener('timeupdate', () => {
            const progress = Math.floor((video.currentTime / video.duration) * 100);
            if (progress > 0 && progress % 25 === 0) { // 25%, 50%, 75%, 100%
                trackVideoEvent('progress', videoId, {
                    progress: progress,
                    currentTime: video.currentTime
                });
            }
        });
    }
});

// Очистка при выгрузке страницы
window.addEventListener('beforeunload', function() {
    if (notificationUpdateInterval) {
        clearInterval(notificationUpdateInterval);
    }
});
