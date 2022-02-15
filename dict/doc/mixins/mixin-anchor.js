/**
 * @file anchor mixin
 * @author wheel-w
 */

import { getActualTop } from '@/common/util'

export default {
    watch: {
        $route (to, from) {
            const anchor = to.query.anchor
            if (!anchor) {
                window.scrollTo(0, 0)
                return
            }
            setTimeout(() => {
                this.jumpAnchor(anchor)
            }, 0)
        }
    },
    mounted () {
        const self = this
        document.querySelector('.app-content').addEventListener('click', e => {
            if (e.target.tagName.toUpperCase() === 'A') {
                const anchorLink = e.target.getAttribute('anchor-link')
                if (!anchorLink) {
                    return
                }
                e.preventDefault()
                e.stopPropagation()
                self.$router.push({
                    name: self.$route.name,
                    query: {
                        anchor: anchorLink
                    }
                })
            }
        })

        const anchor = this.$route.query.anchor
        if (!anchor) {
            return
        }
        this.jumpAnchor(anchor)
    },
    methods: {
        jumpAnchor (anchor) {
            const node = document.getElementById(anchor)
            if (!node) {
                window.scrollTo(0, 0)
                return
            }
            const top = getActualTop(node)
            setTimeout(() => {
                window.scrollTo(0, top - 70)
                // window.scrollTo({
                //     top: top - 70,
                //     behavior: 'smooth'
                // })
            }, 0)
        }
    }
}
