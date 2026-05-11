document.addEventListener('DOMContentLoaded', () => {
	const body = document.body;
	const sidebar = document.getElementById('sidebar');
	const overlay = document.getElementById('sidebarOverlay');
	const menuToggle = document.getElementById('menuToggle');
	const sidebarClose = document.getElementById('sidebarClose');
	const navLinks = Array.from(document.querySelectorAll('.nav-link'));
	const deleteLinks = Array.from(document.querySelectorAll('.btn-delete'));

	const openSidebar = () => {
		if (!sidebar || !overlay || !menuToggle) return;
		sidebar.classList.add('is-open');
		overlay.classList.add('is-open');
		body.classList.add('sidebar-open');
		menuToggle.setAttribute('aria-expanded', 'true');
	};

	const closeSidebar = () => {
		if (!sidebar || !overlay || !menuToggle) return;
		sidebar.classList.remove('is-open');
		overlay.classList.remove('is-open');
		body.classList.remove('sidebar-open');
		menuToggle.setAttribute('aria-expanded', 'false');
	};

	if (menuToggle) {
		menuToggle.addEventListener('click', () => {
			if (sidebar && sidebar.classList.contains('is-open')) {
				closeSidebar();
			} else {
				openSidebar();
			}
		});
	}

	if (sidebarClose) {
		sidebarClose.addEventListener('click', closeSidebar);
	}

	if (overlay) {
		overlay.addEventListener('click', closeSidebar);
	}

	navLinks.forEach((link) => {
		link.addEventListener('click', () => {
			if (window.matchMedia('(max-width: 960px)').matches) {
				closeSidebar();
			}
		});
	});

	deleteLinks.forEach((link) => {
		link.addEventListener('click', (event) => {
			const label = link.closest('tr')?.querySelector('td:nth-child(2), td:nth-child(3)')?.textContent?.trim() || 'este registro';
			const confirmed = window.confirm(`¿Seguro que deseas eliminar ${label}?`);

			if (!confirmed) {
				event.preventDefault();
			}
		});
	});

	const currentPath = window.location.pathname.replace(/\/$/, '') || '/';

	navLinks.forEach((link) => {
		const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, '') || '/';
		const matches = currentPath === linkPath || currentPath.startsWith(linkPath + '/');
		if (matches) {
			link.classList.add('active');
		}
	});
});
