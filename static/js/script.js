document.addEventListener('DOMContentLoaded', function() {
    // ===== HEADER SCROLL EFFECT =====
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });

    // ===== PARALLAX HERO =====
    const hero = document.querySelector('.hero');
    if (hero) {
        // Включаем параллакс только для десктопов (где нет тача)
        if (!('ontouchstart' in window)) {
            let ticking = false;
            const updateParallax = () => {
                const scrolled = window.scrollY;
                hero.style.backgroundPositionY = `${-(scrolled * 0.3)}px`;
                ticking = false;
            };

            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(updateParallax);
                    ticking = true;
                }
            });
            // Вызываем сразу, чтобы при загрузке на середине страницы не было прыжка
            updateParallax();
        }
    }

    // ===== MOBILE MENU =====
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            nav.classList.toggle('active');
            // Блокируем скролл body при открытом меню для предотвращения артефактов
            document.body.classList.toggle('no-scroll');
        });
        document.querySelectorAll('.nav__link').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                nav.classList.remove('active');
                document.body.classList.remove('no-scroll');
            });
        });
    }

    // ===== ACTIVE NAV LINK =====
    const navLinks = document.querySelectorAll('.nav__link');
    const currentPath = location.pathname; // Например: '/', '/menu/', '/gallery/'

    document.querySelectorAll('.nav__link').forEach(link => {
        let linkHref = link.getAttribute('href'); // Например: '/', '/menu/', '/gallery/'

        // Удаляем конечный слеш для сравнения, если это не корневой путь '/'
        const normalizedCurrentPath = (currentPath.length > 1 && currentPath.endsWith('/')) ? currentPath.slice(0, -1) : currentPath;
        const normalizedLinkHref = (linkHref.length > 1 && linkHref.endsWith('/')) ? linkHref.slice(0, -1) : linkHref;

        if (normalizedCurrentPath === normalizedLinkHref) {
            link.classList.add('active');
        }
    });


    // ===== GALLERY LIGHTBOX =====
    const galleryItems = document.querySelectorAll('.gallery-item');
    if (galleryItems.length) {
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-overlay"></div>
            <div class="lightbox-container">
                <button class="lightbox-close"><i class="fas fa-times"></i></button>
                <div class="lightbox-content">
                    <img src="" alt="">
                </div>
                <div class="lightbox-footer">
                    <h3 class="lightbox-title"></h3>
                    <p class="lightbox-desc"></p>
                </div>
            </div>
            <span class="lightbox-prev"><i class="fas fa-chevron-left"></i></span>
            <span class="lightbox-next"><i class="fas fa-chevron-right"></i></span>
        `;
        document.body.appendChild(lightbox);

        const lightboxImg = lightbox.querySelector('img');
        const lightboxTitle = lightbox.querySelector('.lightbox-title');
        const lightboxDesc = lightbox.querySelector('.lightbox-desc');
        const closeBtn = lightbox.querySelector('.lightbox-close');
        const prevBtn = lightbox.querySelector('.lightbox-prev');
        const nextBtn = lightbox.querySelector('.lightbox-next');
        const overlay = lightbox.querySelector('.lightbox-overlay');

        let currentIndex = 0;
        const itemsData = Array.from(galleryItems).map(item => ({
            src: item.querySelector('img').src,
            title: item.querySelector('.gallery-title')?.textContent || '',
            desc: item.querySelector('.gallery-description')?.textContent || ''
        }));

        function showLightbox(index) {
            if (index >= 0 && index < itemsData.length) {
                const data = itemsData[index];
                lightboxImg.src = data.src;
                lightboxTitle.textContent = data.title;
                lightboxDesc.textContent = data.desc;
                currentIndex = index;
                lightbox.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        galleryItems.forEach((item, idx) => item.addEventListener('click', () => {
            if (window.innerWidth <= 768 || ('ontouchstart' in window)) { // Открываем лайтбокс только на мобильных или тач-устройствах
                showLightbox(idx);
            }
        }));

        const closeLightbox = () => { lightbox.classList.remove('active'); document.body.style.overflow = ''; };
        closeBtn.addEventListener('click', closeLightbox);
        overlay.addEventListener('click', closeLightbox);
        prevBtn.addEventListener('click', (e) => { e.stopPropagation(); showLightbox((currentIndex - 1 + itemsData.length) % itemsData.length); });
        nextBtn.addEventListener('click', (e) => { e.stopPropagation(); showLightbox((currentIndex + 1) % itemsData.length); });

        document.addEventListener('keydown', (e) => {
            if (!lightbox.classList.contains('active')) return;
            if (e.key === 'Escape') closeLightbox();
            else if (e.key === 'ArrowLeft') showLightbox((currentIndex - 1 + itemsData.length) % itemsData.length);
            else if (e.key === 'ArrowRight') showLightbox((currentIndex + 1) % itemsData.length);
        });
    }

    // ===== NEWS MODAL LOGIC =====
    const newsCards = document.querySelectorAll('.news-card');
    const newsModal = document.getElementById('newsModal');
    
    if (newsCards.length && newsModal) {
        const modalImg = newsModal.querySelector('.news-modal__image img');
        const modalTitle = newsModal.querySelector('.news-modal__title');
        const modalDesc = newsModal.querySelector('.news-modal__desc');
        const modalPromo = newsModal.querySelector('.news-modal__promo');
        const closeBtn = newsModal.querySelector('.news-modal__close');
        const overlay = newsModal.querySelector('.news-modal__overlay');

        newsCards.forEach(card => {
            card.addEventListener('click', () => {
                const data = card.dataset;
                modalImg.src = data.fullImg;
                modalTitle.textContent = data.fullTitle;
                modalDesc.textContent = data.fullDesc;
                
                if (data.promoEnd) {
                    modalPromo.textContent = `Акция действительна до: ${data.promoEnd}`;
                    modalPromo.style.display = 'inline-flex';
                } else {
                    modalPromo.style.display = 'none';
                }
                
                newsModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            });
        });

        const closeModal = () => {
            newsModal.classList.remove('active');
            document.body.style.overflow = '';
        };

        closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', closeModal);
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });
    }

    // ===== SCROLL ANIMATIONS (Intersection Observer) =====
    const animatedElements = document.querySelectorAll('[data-animate]');
    if (animatedElements.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');

                    // Check if it's a stat-item and if it hasn't been counted yet
                    if (entry.target.classList.contains('stat-item') && !entry.target.dataset.counted) {
                        const statValueElement = entry.target.querySelector('.stat-value');
                        if (statValueElement) {
                            const targetValueStr = statValueElement.dataset.targetValue;
                            // Regex для обработки чисел с пробелами/запятыми как разделителями и суффиксами
                            const match = targetValueStr.match(/^([\d\s\.,]+)([a-zA-Z\+]*)$/); 
                            
                            if (match) {
                                const cleanedNumStr = match[1].replace(/[\s,]/g, ''); // Удаляем пробелы и запятые
                                const targetNum = parseFloat(cleanedNumStr); // Преобразуем в число
                                const suffix = match[2] || '';
                                
                                let start = 0;
                                const duration = 2000; // Длительность анимации в миллисекундах (2 секунды)
                                const startTime = performance.now();

                                const animateCount = (currentTime) => {
                                    const progress = (currentTime - startTime) / duration;
                                    const current = Math.min(progress, 1) * targetNum;
                                    statValueElement.textContent = Math.floor(current) + suffix;

                                    if (progress < 1) {
                                        requestAnimationFrame(animateCount);
                                    } else {
                                        statValueElement.textContent = targetValueStr; // Убедимся, что конечное значение точное
                                    }
                                };
                                requestAnimationFrame(animateCount);
                                entry.target.dataset.counted = 'true'; // Помечаем элемент как посчитанный, чтобы не анимировать повторно
                            } else {
                                // Если значение не является числом (например, просто текст), просто отображаем его
                                statValueElement.textContent = targetValueStr;
                                entry.target.dataset.counted = 'true'; // Помечаем как отображенный
                            }
                        }
                    }
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });
        animatedElements.forEach(el => observer.observe(el));
    }

    // ===== FORMS =====
    const validatePhone = (phone) => {
        // Более гибкое правило: разрешаем цифры, пробелы, скобки и +, длиной от 7 до 18 символов
        const phoneRegex = /^[0-9\s\+\-\(\)]{7,18}$/;
        return phoneRegex.test(phone);
    };

    const reservationForm = document.getElementById('reservationForm');
    if (reservationForm) {
        reservationForm.addEventListener('submit', (e) => {
            const phoneInput = reservationForm.querySelector('input[name="phone"]');
            if (phoneInput && !validatePhone(phoneInput.value)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный номер телефона (только цифры).');
                phoneInput.focus();
            }
        });
    }

    // Ищем форму контактов по ID (пробуем разные варианты написания)
    const contactForm = document.getElementById('contactForm') || document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            const phoneInput = contactForm.querySelector('input[name="phone"]');
            if (phoneInput && phoneInput.value && !validatePhone(phoneInput.value)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный номер телефона.');
                phoneInput.focus();
            }
        });
    }

    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            // Убираем e.preventDefault(), чтобы данные ушли в Django
        });
    }

    // Set min date for reservation
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput) dateInput.min = new Date().toISOString().split('T')[0];

    // ===== MENU FILTER ACTIVE MARKER =====
    const menuFilter = document.querySelector('.menu-filter');
    const filterButtons = document.querySelectorAll('.filter-button');
    const activeMarker = document.querySelector('.menu-filter__active-marker');

    if (menuFilter && filterButtons.length && activeMarker) {
        const positionMarker = (button, skipTransition = false) => {
            if (button) {
                if (skipTransition) {
                    activeMarker.style.transition = 'none';
                } else {
                    activeMarker.style.transition = ''; // Возвращаем CSS-переход
                }

                const filterRect = menuFilter.getBoundingClientRect();
                const buttonRect = button.getBoundingClientRect();

                // Вычисляем позицию относительно родителя
                const offset = 5; // Смещение в пикселях: чем больше число, тем "худее" будет метка
                const x = buttonRect.left - filterRect.left + offset;
                const y = buttonRect.top - filterRect.top + offset;
                const width = buttonRect.width - (offset * 2);
                const height = buttonRect.height - (offset * 2);

                // Устанавливаем размеры и позицию метки
                activeMarker.style.width = `${width}px`;
                activeMarker.style.height = `${height}px`;
                activeMarker.style.transform = `translate(${x}px, ${y}px)`;
                activeMarker.style.opacity = '1';

                // Если отключали анимацию, принудительно вызываем перерисовку
                if (skipTransition) {
                    activeMarker.offsetHeight; 
                }
            } else {
                activeMarker.style.opacity = '0';
            }
        };

        // Инициализация: ставим метку сразу без анимации
        const activeBtn = menuFilter.querySelector('.filter-button.active');
        if (activeBtn) {
            // Первый расчет
            requestAnimationFrame(() => positionMarker(activeBtn, true));
            
            // Повторный расчет после полной загрузки страницы (включая шрифты)
            window.addEventListener('load', () => positionMarker(activeBtn, true));
        }

        // Обновление при ресайзе
        window.addEventListener('resize', () => positionMarker(menuFilter.querySelector('.filter-button.active')));

        // Плавное перемещение и AJAX-загрузка
        filterButtons.forEach(btn => {
            btn.addEventListener('click', async function(e) {
                const href = this.getAttribute('href');
                if (href && !this.classList.contains('active')) {
                    e.preventDefault();
                    
                    // Визуально двигаем метку сразу
                    positionMarker(this); 
                    filterButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    // Загружаем контент
                    try {
                        const response = await fetch(href);
                        const html = await response.text();
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        
                        const newContent = doc.getElementById('menu-container');
                        const currentContainer = document.getElementById('menu-container');
                        
                        if (newContent && currentContainer) {
                            currentContainer.innerHTML = newContent.innerHTML;
                            cart.updateUI(); // Обновляем кнопки корзины после AJAX-загрузки меню
                            // Обновляем URL в строке браузера без перезагрузки
                            history.pushState(null, '', href);
                        }
                    } catch (err) {
                        window.location.href = href; // Если что-то пошло не так, просто переходим
                    }
                }
            });
        });
    }
});

// ===== CART SYSTEM =====
const cart = {
    items: JSON.parse(localStorage.getItem('restaurant_cart')) || [],

    save() {
        localStorage.setItem('restaurant_cart', JSON.stringify(this.items));
        this.updateUI();
    },

    add(id, title, price, oldPrice = null) {
        const existingItem = this.items.find(item => item.id === id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({ id, title, price: parseFloat(price), oldPrice: oldPrice ? parseFloat(oldPrice) : null, quantity: 1 });
        }
        this.save();
        
        // Маленькая анимация кнопки корзины
        const btn = document.getElementById('cartToggleBtn');
        if (btn) {
            btn.classList.add('pulse-anim');
            setTimeout(() => btn.classList.remove('pulse-anim'), 500);
        }
    },

    updateQuantity(id, delta) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            item.quantity += delta;
            if (item.quantity <= 0) {
                this.items = this.items.filter(i => i.id !== id);
            }
            this.save();
        }
    },

    clear() {
        if (this.items.length === 0) return;
        if (confirm('Вы уверены, что хотите полностью очистить корзину?')) {
            this.items = [];
            this.save();
        }
    },

    toggle() {
        const modal = document.getElementById('cartModal');
        if (!modal) return;
        modal.classList.toggle('active');
        if (modal.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    },

    updateUI() {
        const cartItemsContainer = document.getElementById('cartItems');
        const cartBadge = document.getElementById('cartBadge');
        const totalValue = document.getElementById('cartTotalValue');
        const orderBtn = document.getElementById('whatsappOrderBtn');
        const clearHeader = document.getElementById('cartClearHeader');
        const cardControls = document.querySelectorAll('.cart-control-wrapper');

        let total = 0;
        let count = 0;

        if (!cartItemsContainer) return;

        if (cartItemsContainer) {
            if (this.items.length === 0) {
                cartItemsContainer.innerHTML = '<div class="cart-empty-msg">Ваша корзина пуста</div>';
                if (orderBtn) orderBtn.style.display = 'none';
                if (clearHeader) clearHeader.style.display = 'none';
            } else {
                if (orderBtn) orderBtn.style.display = 'block';
                if (clearHeader) clearHeader.style.display = 'flex';
                cartItemsContainer.innerHTML = this.items.map(item => {
                    total += item.price * item.quantity;
                    count += item.quantity;
                    
                    const hasPromo = item.oldPrice && item.oldPrice > item.price;
                    const priceHTML = hasPromo 
                        ? `<span class="cart-item__price--old">${item.oldPrice}</span> <span class="cart-item__price--new">${item.price} сом</span>`
                        : `<span class="cart-item__price">${item.price} сом</span>`;

                    return `
                        <div class="cart-item">
                            <div class="cart-item__info">
                                <div class="cart-item__title">${item.title}</div>
                                <div class="cart-item__price-box">${priceHTML}</div>
                            </div>
                            <div class="cart-item__controls">
                                <button onclick="cart.updateQuantity('${item.id}', -1)">-</button>
                                <span>${item.quantity}</span>
                                <button onclick="cart.updateQuantity('${item.id}', 1)">+</button>
                            </div>
                        </div>
                    `;
                }).join('');
            }
        }

        if (cartBadge) {
            cartBadge.textContent = count;
            cartBadge.style.display = count > 0 ? 'flex' : 'none';
        }
        if (totalValue) {
            totalValue.textContent = total.toLocaleString();
        }

        // Обновляем все кнопки на карточках
        cardControls.forEach(wrapper => {
            const dishId = wrapper.dataset.dishId;
            const dishTitle = wrapper.dataset.dishTitle;
            const dishPrice = wrapper.dataset.dishPrice;
            const dishOldPrice = wrapper.dataset.dishOldPrice;
            const item = this.items.find(i => i.id === dishId);

            if (item && item.quantity > 0) {
                wrapper.innerHTML = `
                    <div class="dish-card__cart-controls">
                        <button class="btn-qty-sm" onclick="cart.updateQuantity('${dishId}', -1)"><i class="fas fa-minus"></i></button>
                        <span class="dish-card__qty-num">${item.quantity}</span>
                        <button class="btn-qty-sm" onclick="cart.updateQuantity('${dishId}', 1)"><i class="fas fa-plus"></i></button>
                    </div>
                `;
            } else {
                wrapper.innerHTML = `
                    <button class="btn-add-cart" title="Добавить в корзину" 
                            onclick="cart.add('${dishId}', '${dishTitle}', ${dishPrice}, ${dishOldPrice})">
                        <i class="fas fa-plus"></i>
                    </button>
                `;
            }
        });
    },

    sendOrder(phone) {
        if (this.items.length === 0) return;

        let message = "Здравствуйте! Хочу заказать:\n\n";
        let total = 0;

        this.items.forEach((item, index) => {
            const sum = item.price * item.quantity;
            message += `${index + 1}. ${item.title} — ${item.quantity} шт. (${sum} сом)\n`;
            total += sum;
        });

        message += `\n*Итого: ${total} сом*`;
        
        const encodedMessage = encodeURIComponent(message);
        const url = `https://wa.me/${phone}?text=${encodedMessage}`;
        window.open(url, '_blank');
    }
};

// Инициализация UI при загрузке
document.addEventListener('DOMContentLoaded', () => cart.updateUI());