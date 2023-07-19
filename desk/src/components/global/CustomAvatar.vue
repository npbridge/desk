<template>
  <div class="overflow-hidden" :class="styleClasses">
    <img
      v-if="
        imageURL && imageOwner
          ? imageOwner === user.user
            ? imageURL
            : !imageURL.includes('private') && imageURL
          : imageURL
      "
      :src="imageURL"
      class="object-cover"
      :class="styleClasses"
    />
    <div
      v-else
      class="flex items-center justify-center w-full h-full text-gray-600 uppercase bg-gray-200"
      :class="
        { xs: 'text-xs', sm: 'text-sm', md: 'text-base', lg: 'text-lg' }[size]
      "
    >
      {{ label && label[0] }}
    </div>
  </div>
</template>

<script>
import { inject } from 'vue'

const validShapes = ['square', 'circle']

export default {
  name: 'CustomAvatar',
  props: {
    imageURL: String,
    label: String,
    imageOwner: String,
    size: {
      default: '8',
    },
    shape: {
      default: 'circle',
      validator(value) {
        const valid = validShapes.includes(value)
        if (!valid) {
        }
        return valid
      },
    },
  },
  setup() {
    const user = inject('user')

    return { user }
  },
  computed: {
    styleClasses() {
      const sizeClasses = {
        xs: 'h-5 w-5',
        sm: 'h-6 w-6',
        md: 'h-7 w-7',
        lg: 'h-8 w-8',
        xl: 'h-10 w-10',
        '2xl': 'h-12 w-12',
      }[this.size]

      const shapeClass = {
        circle: 'rounded-full',
        square: 'rounded-lg',
      }[this.shape]

      return `${shapeClass} ${sizeClasses}`
    },
  },
}
</script>
