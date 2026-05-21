document.addEventListener('DOMContentLoaded', function () {
    const tabHeaders = document.querySelector('.index-tab-headers')
    const tabContents = document.querySelectorAll('.index-tab-content')
    if (!tabHeaders || !tabContents.length) return

    const buttons = Array.from(tabHeaders.querySelectorAll('button'))

    function setActiveTab(tabId) {
        buttons.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId))
        tabContents.forEach(content => content.classList.toggle('active', content.dataset.tab === tabId))
    }

    tabHeaders.addEventListener('click', function (event) {
        const clicked = event.target.closest('button')
        if (!clicked || !clicked.dataset.tab) return
        setActiveTab(clicked.dataset.tab)
    })
})
