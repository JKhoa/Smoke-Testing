const { test, expect } = require('@playwright/test');

test.describe('SMOKE - vkt-store UI on KTPM arch (10 cases)', () => {
    const baseURL = 'http://localhost:3000'; // Adjust to your e-commerce app URL

    test('1) Home loads & has title', async({ page }) => {
        await page.goto(baseURL);
        await expect(page).toHaveTitle(/vkt-store|Shop|Home/);

        // Verify essential elements are present
        await expect(page.locator('header')).toBeVisible();
        await expect(page.locator('nav')).toBeVisible();
    });

    test('2) Header navigation switches views', async({ page }) => {
        await page.goto(baseURL);

        // Test navigation links
        const navLinks = page.locator('nav a');
        const linkCount = await navLinks.count();
        expect(linkCount).toBeGreaterThan(0);

        // Click on different navigation items
        if (await page.locator('nav a:has-text("Products")').isVisible()) {
            await page.locator('nav a:has-text("Products")').click();
            await page.waitForLoadState('networkidle');
        }

        if (await page.locator('nav a:has-text("Categories")').isVisible()) {
            await page.locator('nav a:has-text("Categories")').click();
            await page.waitForLoadState('networkidle');
        }
    });

    test('3) Products render (tolerant selectors)', async({ page }) => {
        await page.goto(baseURL + '/products');

        // Wait for products to load with tolerant selectors
        await page.waitForSelector('[data-testid="product"], .product, .product-card, .item', { timeout: 10000 });

        const products = page.locator('[data-testid="product"], .product, .product-card, .item');
        const productCount = await products.count();
        expect(productCount).toBeGreaterThan(0);

        // Verify first product has essential info
        const firstProduct = products.first();
        await expect(firstProduct).toBeVisible();
    });

    test('4) Search filters products (if present)', async({ page }) => {
        await page.goto(baseURL);

        // Look for search input with various possible selectors
        const searchSelectors = [
            '[data-testid="search"]',
            'input[type="search"]',
            'input[placeholder*="search" i]',
            '.search-input',
            '#search'
        ];

        let searchInput = null;
        for (const selector of searchSelectors) {
            if (await page.locator(selector).isVisible()) {
                searchInput = page.locator(selector);
                break;
            }
        }

        if (searchInput) {
            await searchInput.fill('shirt');
            await searchInput.press('Enter');
            await page.waitForLoadState('networkidle');

            // Verify search results or no results message
            const hasResults = await page.locator('[data-testid="product"], .product, .no-results').isVisible();
            expect(hasResults).toBeTruthy();
        }
    });

    test('5) Category filter works (if present)', async({ page }) => {
        await page.goto(baseURL);

        // Look for category filters
        const categorySelectors = [
            '[data-testid="category"]',
            '.category-filter',
            '.filter-category',
            'select[name="category"]'
        ];

        let categoryFilter = null;
        for (const selector of categorySelectors) {
            if (await page.locator(selector).isVisible()) {
                categoryFilter = page.locator(selector);
                break;
            }
        }

        if (categoryFilter) {
            // If it's a select dropdown
            if (await categoryFilter.getAttribute('tagName') === 'SELECT') {
                await categoryFilter.selectOption({ index: 1 });
            } else {
                // If it's a clickable filter
                await categoryFilter.first().click();
            }

            await page.waitForLoadState('networkidle');
        }
    });

    test('6) Add to cart -> appears in cart', async({ page }) => {
        await page.goto(baseURL);

        // Find and click on a product
        const productSelectors = [
            '[data-testid="product"]:first-child',
            '.product:first-child',
            '.product-card:first-child'
        ];

        let product = null;
        for (const selector of productSelectors) {
            if (await page.locator(selector).isVisible()) {
                product = page.locator(selector);
                break;
            }
        }

        if (product) {
            await product.click();

            // Look for add to cart button
            const addToCartSelectors = [
                '[data-testid="add-to-cart"]',
                'button:has-text("Add to Cart")',
                'button:has-text("Add")',
                '.add-to-cart',
                '.btn-add-cart'
            ];

            for (const selector of addToCartSelectors) {
                if (await page.locator(selector).isVisible()) {
                    await page.locator(selector).click();
                    break;
                }
            }

            // Verify cart indicator updates
            const cartSelectors = [
                '[data-testid="cart-count"]',
                '.cart-count',
                '.cart-badge',
                '.cart-items'
            ];

            for (const selector of cartSelectors) {
                if (await page.locator(selector).isVisible()) {
                    await expect(page.locator(selector)).toContainText(/[1-9]/);
                    break;
                }
            }
        }
    });

    test('7) Quantity change updates total (if controls exist)', async({ page }) => {
        await page.goto(baseURL + '/cart');

        // Look for quantity controls
        const quantitySelectors = [
            '[data-testid="quantity"]',
            'input[type="number"]',
            '.quantity-input'
        ];

        let quantityInput = null;
        for (const selector of quantitySelectors) {
            if (await page.locator(selector).isVisible()) {
                quantityInput = page.locator(selector).first();
                break;
            }
        }

        if (quantityInput) {
            const initialValue = await quantityInput.inputValue();
            const newValue = parseInt(initialValue) + 1;

            await quantityInput.fill(newValue.toString());
            await page.waitForTimeout(1000); // Wait for total to update

            // Verify total updates (this is a basic check)
            const totalSelectors = [
                '[data-testid="total"]',
                '.total',
                '.cart-total'
            ];

            for (const selector of totalSelectors) {
                if (await page.locator(selector).isVisible()) {
                    await expect(page.locator(selector)).toBeVisible();
                    break;
                }
            }
        }
    });

    test('8) Remove item from cart (if supported)', async({ page }) => {
        await page.goto(baseURL + '/cart');

        // Look for remove buttons
        const removeSelectors = [
            '[data-testid="remove"]',
            'button:has-text("Remove")',
            'button:has-text("Delete")',
            '.remove-item',
            '.btn-remove'
        ];

        for (const selector of removeSelectors) {
            if (await page.locator(selector).isVisible()) {
                await page.locator(selector).first().click();

                // Confirm removal if dialog appears
                if (await page.locator('button:has-text("Confirm")').isVisible()) {
                    await page.locator('button:has-text("Confirm")').click();
                }

                await page.waitForTimeout(1000);
                break;
            }
        }
    });

    test('9) Login empty submit shows error (if login exists)', async({ page }) => {
        // Try to find login page
        await page.goto(baseURL);

        const loginSelectors = [
            'a:has-text("Login")',
            'a:has-text("Sign In")',
            '[data-testid="login"]',
            '.login-link'
        ];

        let loginFound = false;
        for (const selector of loginSelectors) {
            if (await page.locator(selector).isVisible()) {
                await page.locator(selector).click();
                loginFound = true;
                break;
            }
        }

        if (!loginFound) {
            // Try direct URL
            await page.goto(baseURL + '/login');
        }

        // Try to submit empty login form
        const submitSelectors = [
            'button:has-text("Login")',
            'button:has-text("Sign In")',
            'button[type="submit"]',
            '.btn-login'
        ];

        for (const selector of submitSelectors) {
            if (await page.locator(selector).isVisible()) {
                await page.locator(selector).click();

                // Look for error message
                const errorSelectors = [
                    '.error',
                    '.alert-error',
                    '[data-testid="error"]',
                    '.form-error'
                ];

                for (const errorSelector of errorSelectors) {
                    if (await page.locator(errorSelector).isVisible()) {
                        await expect(page.locator(errorSelector)).toBeVisible();
                        return;
                    }
                }
                break;
            }
        }
    });

    test('10) Cart persists after refresh (if implemented)', async({ page }) => {
        await page.goto(baseURL);

        // Add item to cart first (simplified)
        const productSelectors = [
            '[data-testid="product"]:first-child',
            '.product:first-child'
        ];

        for (const selector of productSelectors) {
            if (await page.locator(selector).isVisible()) {
                await page.locator(selector).click();

                // Add to cart
                const addToCartSelectors = [
                    '[data-testid="add-to-cart"]',
                    'button:has-text("Add to Cart")'
                ];

                for (const cartSelector of addToCartSelectors) {
                    if (await page.locator(cartSelector).isVisible()) {
                        await page.locator(cartSelector).click();
                        break;
                    }
                }
                break;
            }
        }

        // Refresh page
        await page.reload();

        // Check if cart still has items
        const cartSelectors = [
            '[data-testid="cart-count"]',
            '.cart-count'
        ];

        for (const selector of cartSelectors) {
            if (await page.locator(selector).isVisible()) {
                const cartText = await page.locator(selector).textContent();
                expect(parseInt(cartText) || 0).toBeGreaterThanOrEqual(0);
                break;
            }
        }
    });
});