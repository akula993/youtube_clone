// Основной JavaScript для YouTube Clone

$(document).ready(function() {
    // Автоматическое скрытие уведомлений
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Инициализация tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Обработка фокуса комментария
    $('textarea[name="content"]').focus(function() {
        $(this).attr('rows', 3);
        $(this).parent().siblings('.comment-actions').show();
    });
    
    $('.cancel-comment').click(function() {
        const textarea = $(this).parent().siblings('.form-group').find('textarea');
        textarea.attr('rows', 1);
        textarea.val('');
        $(this).parent().hide();
    });
    
    // Автоматическое изменение размера textarea
    $('textarea').on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Функция для показа уведомлений
    window.showNotification = function(message, type) {
        const notification = $(`
            <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(function() {
            notification.fadeOut(function() {
                $(this).remove();
            });
        }, 5000);
    };
});

// Функции утилиты
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
