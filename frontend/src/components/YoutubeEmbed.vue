<template>
  <div ref="playerContainer"></div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  url: String
})
const emit = defineEmits(['ended'])

const playerContainer = ref(null)
const player = ref(null)

const getVideoId = (url) => {
  const match = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/))([\w-]+)/)
  return match ? match[1] : null
}

const createPlayer = () => {
  const videoId = getVideoId(props.url)
  if (!videoId) return

  if (player.value) {
    player.value.loadVideoById(videoId)
    return
  }

  player.value = new YT.Player(playerContainer.value, {
    height: '360',
    width: '640',
    videoId,
    playerVars: {
      rel: 0,
      modestbranding: 1,
      autoplay: 1,
      controls: 1,
    },
    events: {
      onStateChange: (event) => {
        if (event.data === YT.PlayerState.ENDED) {
          emit('ended')
        }
      }
    }
  })
}

watch(() => props.url, () => {
  createPlayer()
})

onMounted(() => {
  if (!window.YT) {
    const tag = document.createElement('script')
    tag.src = 'https://www.youtube.com/iframe_api'
    document.body.appendChild(tag)
    window.onYouTubeIframeAPIReady = createPlayer
  } else {
    createPlayer()
  }
})

onBeforeUnmount(() => {
  if (player.value && player.value.destroy) {
    player.value.destroy()
  }
})
</script>
