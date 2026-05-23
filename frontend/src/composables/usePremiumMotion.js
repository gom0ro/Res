/** Shared motion presets (Framer-style) for @vueuse/motion */
export const fadeUp = {
  initial: { opacity: 0, y: 14 },
  enter: {
    opacity: 1,
    y: 0,
    transition: { duration: 450, ease: [0.22, 1, 0.36, 1] },
  },
}

export const fadeIn = {
  initial: { opacity: 0 },
  enter: {
    opacity: 1,
    transition: { duration: 350, ease: [0.22, 1, 0.36, 1] },
  },
}

export const staggerEnter = (index, baseDelay = 0, step = 55) => ({
  initial: { opacity: 0, y: 12 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      delay: baseDelay + index * step,
      duration: 400,
      ease: [0.22, 1, 0.36, 1],
    },
  },
})

export const cardHover = {
  hovered: {
    y: -2,
    transition: { duration: 250, ease: [0.22, 1, 0.36, 1] },
  },
}
