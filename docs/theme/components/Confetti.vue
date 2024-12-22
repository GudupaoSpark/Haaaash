<script setup lang="ts">
import confetti from "canvas-confetti";

/* 纸屑 */
confetti({
  particleCount: 500,
  spread: 160,
  origin: { y: 0.6 },
});
</script>