(() => {
    const storefront = document.querySelector("#storefront");
    if (!storefront) return;

    const apiUrl = storefront.dataset.apiUrl;
    const grid = document.querySelector("#product-grid");
    const searchInput = document.querySelector("#product-search");
    const sortSelect = document.querySelector("#product-sort");
    const status = document.querySelector("#product-status");
    const emptyState = document.querySelector("#product-empty");
    const categoryLinks = [...document.querySelectorAll("[data-category]")];
    let selectedCategory = storefront.dataset.category || "";
    let requestNumber = 0;
    let searchTimer;

    function setActiveCategory() {
        categoryLinks.forEach((link) => {
            const active = link.dataset.category === selectedCategory;
            link.classList.toggle("active", active);
            if (active) link.setAttribute("aria-current", "true");
            else link.removeAttribute("aria-current");
        });
    }

    function updateAddressBar(historyMethod) {
        const url = new URL(window.location.href);
        if (selectedCategory) url.searchParams.set("category", selectedCategory);
        else url.searchParams.delete("category");
        if (searchInput.value.trim()) url.searchParams.set("q", searchInput.value.trim());
        else url.searchParams.delete("q");
        if (sortSelect.value !== "name") url.searchParams.set("ordering", sortSelect.value);
        else url.searchParams.delete("ordering");
        window.history[historyMethod]({}, "", url);
    }

    function makeProductCard(product) {
        const column = document.createElement("div");
        column.className = "col-xl-4 col-md-6";

        const card = document.createElement("article");
        card.className = "card product-card h-100";

        const imageLink = document.createElement("a");
        imageLink.className = "product-card-image";
        imageLink.href = product.detail_url;
        imageLink.setAttribute("aria-label", `View ${product.name}`);
        if (product.image_url) {
            const image = document.createElement("img");
            image.src = product.image_url;
            image.alt = product.name;
            image.loading = "lazy";
            imageLink.append(image);
        } else {
            const placeholder = document.createElement("span");
            placeholder.className = "product-image-placeholder";
            placeholder.textContent = "No image";
            imageLink.append(placeholder);
        }

        const body = document.createElement("div");
        body.className = "card-body d-flex flex-column";
        const category = document.createElement("p");
        category.className = "small text-muted mb-1";
        category.textContent = product.category.name;
        const title = document.createElement("h3");
        title.className = "h5 card-title";
        title.textContent = product.name;
        const price = document.createElement("p");
        price.className = "product-price mt-auto mb-3";
        price.textContent = `Price: ${product.price}`;
        const detail = document.createElement("a");
        detail.className = "btn btn-dark";
        detail.href = product.detail_url;
        detail.textContent = "View product";

        body.append(category, title, price, detail);
        card.append(imageLink, body);
        column.append(card);
        return column;
    }

    async function loadProducts(historyMethod = "replaceState") {
        const currentRequest = ++requestNumber;
        const url = new URL(apiUrl, window.location.origin);
        const query = searchInput.value.trim();
        if (query) url.searchParams.set("q", query);
        if (selectedCategory) url.searchParams.set("category", selectedCategory);
        url.searchParams.set("ordering", sortSelect.value);

        updateAddressBar(historyMethod);
        status.textContent = "Loading products...";
        try {
            const response = await fetch(url, { headers: { Accept: "application/json" } });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "Could not load products.");
            if (currentRequest !== requestNumber) return;

            const cards = document.createDocumentFragment();
            data.results.forEach((product) => cards.append(makeProductCard(product)));
            grid.replaceChildren(cards);
            emptyState.classList.toggle("d-none", data.count !== 0);
            status.textContent = `${data.count} product${data.count === 1 ? "" : "s"}`;
        } catch (error) {
            if (currentRequest !== requestNumber) return;
            status.textContent = "Products could not be loaded. Please try again.";
            emptyState.classList.add("d-none");
        }
    }

    categoryLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            selectedCategory = link.dataset.category || "";
            storefront.dataset.category = selectedCategory;
            setActiveCategory();
            loadProducts("pushState");
        });
    });

    searchInput.addEventListener("input", () => {
        window.clearTimeout(searchTimer);
        searchTimer = window.setTimeout(loadProducts, 250);
    });
    sortSelect.addEventListener("change", loadProducts);

    window.addEventListener("popstate", () => {
        const url = new URL(window.location.href);
        selectedCategory = url.searchParams.get("category") || "";
        searchInput.value = url.searchParams.get("q") || "";
        sortSelect.value = url.searchParams.get("ordering") || "name";
        storefront.dataset.category = selectedCategory;
        setActiveCategory();
        loadProducts();
    });

    const initialUrl = new URL(window.location.href);
    searchInput.value = initialUrl.searchParams.get("q") || "";
    sortSelect.value = initialUrl.searchParams.get("ordering") || "name";
    setActiveCategory();
})();
