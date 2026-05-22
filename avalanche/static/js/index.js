document.addEventListener('DOMContentLoaded', function () {
    const brandSections = document.querySelectorAll('.brand-section')
    if (!brandSections.length) return

    brandSections.forEach(section => {
        const tabHeaders = section.querySelector('.index-tab-headers')
        const tabContents = section.querySelectorAll('.index-tab-content')
        if (!tabHeaders || !tabContents.length) return

        const buttons = Array.from(tabHeaders.querySelectorAll('button'))

        function setActiveTab(tabId) {
            buttons.forEach(btn => {
                if (btn.dataset.tab === tabId) {
                    btn.classList.add('active')
                } else {
                    btn.classList.remove('active')
                }
            })
            tabContents.forEach(content => {
                if (content.dataset.tab === tabId) {
                    content.classList.add('active')
                    // Reset scroll position to the start when activating a tab
                    content.scrollLeft = 0
                } else {
                    content.classList.remove('active')
                }
            })
        }

        buttons.forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault()
                const tabId = this.dataset.tab
                if (tabId) {
                    setActiveTab(tabId)
                }
            })
        })
        
        // Allow mouse wheel to scroll horizontally when over the content area
        tabContents.forEach(content => {
            content.addEventListener('wheel', function (e) {
                // Only intercept if the event is within this specific content area
                // and prevent default only if we're actually scrolling horizontally
                if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
                    // Check if we can scroll more in the direction
                    const maxScrollLeft = this.scrollWidth - this.clientWidth;
                    const newScrollLeft = this.scrollLeft + e.deltaY;

                    // Only prevent default if we're not at the edges
                    if ((newScrollLeft > 0 && newScrollLeft < maxScrollLeft) || (newScrollLeft <= 0 && this.scrollLeft > 0) || (newScrollLeft >= maxScrollLeft && this.scrollLeft < maxScrollLeft)) {
                        e.preventDefault();
                        this.scrollLeft = Math.max(0, Math.min(maxScrollLeft, newScrollLeft));
                    }
                }
            }, { passive: false })
        })
    })
})
