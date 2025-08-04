<template>
  <div class="theater-container bg-gray-900 text-white rounded-lg overflow-hidden shadow-2xl">
    <!-- Legend & Controls -->
    <div class="legend-bar bg-gray-800 px-4 py-3 border-b border-gray-700 sticky top-0 z-10">
      <div class="flex justify-between items-center mb-3">
        <div class="flex items-center gap-3">
          <button 
            @click="zoomOut"
            class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition"
          >
            -
          </button>
          <span class="text-sm">{{ Math.round(zoom * 100) }}%</span>
          <button 
            @click="zoomIn"
            class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition"
          >
            +
          </button>
          <button 
            @click="resetZoom"
            class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition"
          >
            Reset
          </button>
        </div>
        
        <div class="text-sm text-gray-400">
          Cuộn để xem tất cả ghế
        </div>
      </div>
      
      <div class="flex flex-wrap justify-center gap-4 text-xs">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-yellow-500 rounded-full border border-yellow-400"></div>
          <span>Đang trống</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-green-500 rounded-full border border-green-400 flex items-center justify-center">
            <span class="text-xs text-white font-bold">✓</span>
          </div>
          <span>Đang chọn</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-red-800 rounded-full border border-red-700 flex items-center justify-center">
            <span class="text-xs text-red-400">✗</span>
          </div>
          <span>Đã bán</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-yellow-200 rounded-full border border-yellow-400"></div>
          <span>Đang giữ</span>
        </div>
      </div>
    </div>

    <!-- Scrollable Theater Content -->
    <div 
      class="theater-viewport h-96 md:h-[500px] lg:h-[600px] overflow-auto bg-gray-900 relative"
      ref="viewport"
    >
      <div 
        class="theater-content p-6"
        :style="{ transform: `scale(${zoom})`, transformOrigin: 'top center' }"
      >
        <!-- Stage -->
        <div class="stage-area py-6 mb-8">
          <div class="flex justify-center">
            <div class="stage bg-gradient-to-b from-gray-300 to-gray-400 text-gray-800 px-20 py-4 rounded-full shadow-lg">
              <div class="text-center">
                <div class="text-lg font-bold">Sân khấu</div>
                <div class="text-xs opacity-75">STAGE</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Floor 1 Label -->
        <div class="text-center mb-6">
          <h3 class="text-lg font-semibold text-gray-300">Tầng 1</h3>
        </div>
        
        <!-- All Rows Container -->
        <div class="rows-container space-y-2 max-w-none mx-auto">
          <!-- Row A (VIP Orange) - 20 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">A</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 20"
                :key="`A-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('A', n)
                ]"
                @click="selectSeat('A', n)"
                @mouseenter="showTooltip('A', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('A', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">A</div>
          </div>

          <!-- Row B (VIP Orange) - 26 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">B</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 26"
                :key="`B-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('B', n)
                ]"
                @click="selectSeat('B', n)"
                @mouseenter="showTooltip('B', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('B', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">B</div>
          </div>

          <!-- Row C (VIP Orange) - 27 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">C</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 27"
                :key="`C-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('C', n)
                ]"
                @click="selectSeat('C', n)"
                @mouseenter="showTooltip('C', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('C', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">C</div>
          </div>

          <!-- Row D (VIP Orange) - 26 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">D</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 26"
                :key="`D-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('D', n)
                ]"
                @click="selectSeat('D', n)"
                @mouseenter="showTooltip('D', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('D', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">D</div>
          </div>

          <!-- Row E (VIP Orange) - 32 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">E</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 32"
                :key="`E-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('E', n),
                  { 'ml-2': n === 26 }
                ]"
                @click="selectSeat('E', n)"
                @mouseenter="showTooltip('E', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('E', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">E</div>
          </div>

          <!-- Row F (VIP Orange) - 32 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">F</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 32"
                :key="`F-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('F', n),
                  { 'ml-2': n === 26 }
                ]"
                @click="selectSeat('F', n)"
                @mouseenter="showTooltip('F', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('F', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">F</div>
          </div>

          <!-- Row G (Orange/Standard) - 32 seats -->
          <div class="seat-row flex items-center justify-center">
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">G</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in 32"
                :key="`G-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass('G', n),
                  { 'ml-2': n === 26 }
                ]"
                @click="selectSeat('G', n)"
                @mouseenter="showTooltip('G', n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay('G', n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">G</div>
          </div>

          <!-- Rows H-O (Green Standard/Economy) with proper aisles -->
          <div 
            v-for="(row, idx) in ['H', 'I', 'K', 'L', 'M', 'N', 'O']"
            :key="row"
            class="seat-row flex items-center justify-center"
          >
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ row }}</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <!-- Left section -->
              <div
                v-for="n in getLeftSectionCount(row)"
                :key="`${row}-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row, n)
                ]"
                @click="selectSeat(row, n)"
                @mouseenter="showTooltip(row, n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row, n) }}
              </div>
              
              <!-- Aisle -->
              <div class="w-6"></div>
              
              <!-- Middle section -->
              <div
                v-for="n in getMiddleSectionCount(row)"
                :key="`${row}-${n + getLeftSectionCount(row)}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row, n + getLeftSectionCount(row))
                ]"
                @click="selectSeat(row, n + getLeftSectionCount(row))"
                @mouseenter="showTooltip(row, n + getLeftSectionCount(row), $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row, n + getLeftSectionCount(row)) }}
              </div>
              
              <!-- Aisle -->
              <div class="w-6"></div>
              
              <!-- Right section -->
              <div
                v-for="n in getRightSectionCount(row)"
                :key="`${row}-${n + getLeftSectionCount(row) + getMiddleSectionCount(row)}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row, n + getLeftSectionCount(row) + getMiddleSectionCount(row))
                ]"
                @click="selectSeat(row, n + getLeftSectionCount(row) + getMiddleSectionCount(row))"
                @mouseenter="showTooltip(row, n + getLeftSectionCount(row) + getMiddleSectionCount(row), $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row, n + getLeftSectionCount(row) + getMiddleSectionCount(row)) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ row }}</div>
          </div>

          <!-- Rows P-Q (Red Economy) with aisles -->
          <div 
            v-for="row in ['P', 'Q']"
            :key="row"
            class="seat-row flex items-center justify-center"
          >
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ row }}</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <!-- Left section -->
              <div
                v-for="n in 6"
                :key="`${row}-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row, n)
                ]"
                @click="selectSeat(row, n)"
                @mouseenter="showTooltip(row, n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row, n) }}
              </div>
              
              <!-- Aisle -->
              <div class="w-4"></div>
              
              <!-- Middle large section -->
              <div
                v-for="n in (row === 'P' ? 36 : 38)"
                :key="`${row}-${n + 6}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row, n + 6),
                  { 'ml-3': n === 19, 'mr-3': n === 19 }
                ]"
                @click="selectSeat(row, n + 6)"
                @mouseenter="showTooltip(row, n + 6, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row, n + 6) }}
              </div>
              
              <!-- Aisle -->
              <div class="w-4"></div>
              
              <!-- Right section -->
              <div
                v-for="n in 6"
                :key="`${row}-${n + (row === 'P' ? 42 : 44)}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row, n + (row === 'P' ? 42 : 44))
                ]"
                @click="selectSeat(row, n + (row === 'P' ? 42 : 44))"
                @mouseenter="showTooltip(row, n + (row === 'P' ? 42 : 44), $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row, n + (row === 'P' ? 42 : 44)) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ row }}</div>
          </div>

          <!-- Row R with VERTICAL LOGE boxes - FIXED -->
          <div class="balcony-section flex items-center justify-center gap-8 my-4">
            <!-- Left Vertical Loge - LG -->
            <div class="loge-left flex flex-col items-center gap-2">
              <div class="text-sm font-bold text-purple-400">LG</div>
              <div class="flex flex-col gap-1">
                <div
                  v-for="n in 4"
                  :key="`LG-L-${n}`"
                  :class="[
                    'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center text-sm font-bold rounded-full border',
                    getSeatColorClass('LG-L', n)
                  ]"
                  @click="selectSeat('LG-L', n)"
                  @mouseenter="showTooltip('LG-L', n, $event)"
                  @mouseleave="hideTooltip"
                >
                  {{ getSeatDisplay('LG-L', n) }}
                </div>
              </div>
            </div>

            <!-- Center R Row -->
            <div class="center-balcony">
              <div class="seat-row flex items-center justify-center">
                <div class="row-label w-6 text-center text-sm font-bold text-gray-400">R</div>
                <div class="seats-container flex items-center justify-center gap-1">
                  <div
                    v-for="n in 19"
                    :key="`R-${n}`"
                    :class="[
                      'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center text-xs font-bold rounded-full border',
                      getSeatColorClass('R', n),
                      { 'ml-3': n === 16 }
                    ]"
                    @click="selectSeat('R', n)"
                    @mouseenter="showTooltip('R', n, $event)"
                    @mouseleave="hideTooltip"
                  >
                    {{ getSeatDisplay('R', n) }}
                  </div>
                </div>
                <div class="row-label w-6 text-center text-sm font-bold text-gray-400">R</div>
              </div>
            </div>

            <!-- Right Vertical Loge - LG -->
            <div class="loge-right flex flex-col items-center gap-2">
              <div class="text-sm font-bold text-purple-400">LG</div>
              <div class="flex flex-col gap-1">
                <div
                  v-for="n in 4"
                  :key="`LG-R-${n}`"
                  :class="[
                    'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center text-sm font-bold rounded-full border',
                    getSeatColorClass('LG-R', n)
                  ]"
                  @click="selectSeat('LG-R', n)"
                  @mouseenter="showTooltip('LG-R', n, $event)"
                  @mouseleave="hideTooltip"
                >
                  {{ getSeatDisplay('LG-R', n) }}
                </div>
              </div>
            </div>
          </div>

          <!-- Upper Rows S-U -->
          <div 
            v-for="(row, idx) in [
              { label: 'S', seats: 28, aisles: [14] },
              { label: 'T', seats: 26, aisles: [8, 18] },
              { label: 'U', seats: 24, aisles: [8, 16] }
            ]"
            :key="row.label"
            class="seat-row flex items-center justify-center"
          >
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ row.label }}</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in row.seats"
                :key="`${row.label}-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(row.label, n),
                  { 'ml-3': row.aisles && row.aisles.includes(n-1) }
                ]"
                @click="selectSeat(row.label, n)"
                @mouseenter="showTooltip(row.label, n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(row.label, n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ row.label }}</div>
          </div>

          <!-- Floor 2 Separator -->
          <div class="floor-separator border-t-2 border-dashed border-gray-600 mt-8 pt-6">
            <div class="text-center mb-6">
              <h3 class="text-lg font-semibold text-gray-300">Tầng 2</h3>
            </div>
          </div>

          <!-- Floor 2 Upper Rows AA, BB -->
          <div 
            v-for="(rowData, idx) in [
              { label: 'AA', seats: 16 },
              { label: 'BB', seats: 18 }
            ]"
            :key="rowData.label"
            class="seat-row flex items-center justify-center"
          >
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ rowData.label }}</div>
            <div class="seats-container flex items-center justify-center gap-1">
              <div
                v-for="n in rowData.seats"
                :key="`${rowData.label}-${n}`"
                :class="[
                  'seat w-6 h-6 transition-all duration-200 cursor-pointer flex items-center justify-center font-bold text-xs rounded-full border',
                  getSeatColorClass(rowData.label, n)
                ]"
                @click="selectSeat(rowData.label, n)"
                @mouseenter="showTooltip(rowData.label, n, $event)"
                @mouseleave="hideTooltip"
              >
                {{ getSeatDisplay(rowData.label, n) }}
              </div>
            </div>
            <div class="row-label w-6 text-center text-sm font-bold text-gray-400 flex-shrink-0">{{ rowData.label }}</div>
          </div>
        </div>

        <!-- Bottom padding -->
        <div class="h-8"></div>
      </div>
    </div>

    <!-- Tooltip -->
    <div
      v-if="tooltip.show"
      class="fixed bg-white text-gray-800 px-3 py-2 rounded-lg shadow-xl border z-50 pointer-events-none text-sm"
      :style="tooltipStyle"
    >
      <div class="font-semibold">{{ tooltip.sectionName }}</div>
      <div class="text-sm text-gray-600">
        Hàng {{ tooltip.row }} - Ghế {{ tooltip.number }}
      </div>
      <div class="font-bold text-blue-600 mt-1">
        {{ formatPrice(tooltip.price) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const emit = defineEmits(['update:selectedSeats'])

const props = defineProps({
  selectedSeats: {
    type: Array,
    default: () => []
  }
})

// State
const selectedSeats = ref([])
const zoom = ref(1)
const viewport = ref(null)
const tooltip = ref({
  show: false,
  row: '',
  number: 0,
  sectionName: '',
  price: 0,
  x: 0,
  y: 0
})

// Seat data structure
const seatStatuses = ref(new Map())

// Price categories
const priceCategories = {
  vip: 2500000,
  standard: 1500000,
  economy: 1000000,
  balcony: 1200000,
  upper: 800000,
  loge: 3000000
}

// Computed
const tooltipStyle = computed(() => ({
  left: `${tooltip.value.x}px`,
  top: `${tooltip.value.y}px`,
  transform: 'translate(-50%, -120%)'
}))

// Methods
const getLeftSectionCount = (row) => {
  const config = {
    'H': 7, 'I': 6, 'K': 6, 'L': 6, 'M': 6, 'N': 5, 'O': 6
  }
  return config[row] || 6
}

const getMiddleSectionCount = (row) => {
  const config = {
    'H': 20, 'I': 22, 'K': 24, 'L': 26, 'M': 28, 'N': 30, 'O': 32
  }
  return config[row] || 20
}

const getRightSectionCount = (row) => {
  const config = {
    'H': 7, 'I': 8, 'K': 8, 'L': 8, 'M': 8, 'N': 9, 'O': 8
  }
  return config[row] || 7
}

const getSeatId = (row, number) => {
  return `${row}-${number}`
}

const getSeatStatus = (row, number) => {
  const id = getSeatId(row, number)
  return seatStatuses.value.get(id) || 'available'
}

const isSelected = (row, number) => {
  const id = getSeatId(row, number)
  return selectedSeats.value.some(s => s.id === id)
}

const getSeatColorClass = (row, number) => {
  const baseClasses = ['border']
  
  if (isSelected(row, number)) {
    return [...baseClasses, 'bg-green-500', 'border-green-400', 'text-white']
  }
  
  const status = getSeatStatus(row, number)
  
  if (status === 'sold') {
    return [...baseClasses, 'bg-red-800', 'border-red-700', 'cursor-not-allowed', 'text-red-400']
  }
  
  if (status === 'reserved') {
    return [...baseClasses, 'bg-yellow-200', 'border-yellow-400', 'text-yellow-800']
  }
  
  // Available seats - color by row category
  if (['A', 'B', 'C', 'D', 'E', 'F'].includes(row)) {
    return [...baseClasses, 'bg-orange-500', 'border-orange-400', 'text-white', 'hover:bg-orange-400']
  }
  if (['G', 'H', 'I', 'K', 'L', 'M', 'N', 'O'].includes(row)) {
    return [...baseClasses, 'bg-green-600', 'border-green-500', 'text-white', 'hover:bg-green-500']
  }
  if (['P', 'Q'].includes(row)) {
    return [...baseClasses, 'bg-red-600', 'border-red-500', 'text-white', 'hover:bg-red-500']
  }
  if (row === 'R') {
    return [...baseClasses, 'bg-blue-500', 'border-blue-400', 'text-white', 'hover:bg-blue-400']
  }
  if (['S', 'T', 'U'].includes(row)) {
    return [...baseClasses, 'bg-purple-500', 'border-purple-400', 'text-white', 'hover:bg-purple-400']
  }
  if (row.startsWith('LG')) {
    return [...baseClasses, 'bg-purple-600', 'border-purple-500', 'text-white', 'hover:bg-purple-500']
  }
  if (['AA', 'BB'].includes(row)) {
    return [...baseClasses, 'bg-green-600', 'border-green-500', 'text-white', 'hover:bg-green-500']
  }
  
  return [...baseClasses, 'bg-gray-500', 'border-gray-400', 'text-white', 'hover:bg-gray-400']
}

const getSeatDisplay = (row, number) => {
  if (isSelected(row, number)) {
    return number
  }
  
  const status = getSeatStatus(row, number)
  if (status === 'sold') {
    return '✗'
  }
  
  return number
}

const selectSeat = (row, number) => {
  const status = getSeatStatus(row, number)
  if (status !== 'available') return
  
  const id = getSeatId(row, number)
  const seatData = {
    id: id,
    row: row,
    number: number,
    sectionName: getSectionName(row),
    price: getSeatPrice(row)
  }
  
  const index = selectedSeats.value.findIndex(s => s.id === id)
  
  if (index > -1) {
    selectedSeats.value.splice(index, 1)
  } else {
    if (selectedSeats.value.length >= 8) {
      alert('Bạn chỉ có thể chọn tối đa 8 ghế')
      return
    }
    selectedSeats.value.push(seatData)
  }
  
  emit('update:selectedSeats', selectedSeats.value)
}

const getSectionName = (row) => {
  if (['A', 'B', 'C', 'D', 'E', 'F'].includes(row)) return 'VIP'
  if (['G', 'H', 'I', 'K', 'L', 'M', 'N', 'O'].includes(row)) return 'Standard'
  if (['P', 'Q'].includes(row)) return 'Economy'
  if (row === 'R') return 'Balcony'
  if (['S', 'T', 'U'].includes(row)) return 'Upper'
  if (row.startsWith('LG')) return 'Loge'
  if (['AA', 'BB'].includes(row)) return 'Upper Floor 2'
  return 'Standard'
}

const getSeatPrice = (row) => {
  if (['A', 'B', 'C', 'D', 'E', 'F'].includes(row)) return priceCategories.vip
  if (['G', 'H', 'I', 'K', 'L', 'M', 'N', 'O'].includes(row)) return priceCategories.standard
  if (['P', 'Q'].includes(row)) return priceCategories.economy
  if (row === 'R') return priceCategories.balcony
  if (['S', 'T', 'U'].includes(row)) return priceCategories.upper
  if (row.startsWith('LG')) return priceCategories.loge
  if (['AA', 'BB'].includes(row)) return priceCategories.upper
  return priceCategories.standard
}

const showTooltip = (row, number, event) => {
  const status = getSeatStatus(row, number)
  if (status === 'sold') return
  
  const rect = event.currentTarget.getBoundingClientRect()
  tooltip.value = {
    show: true,
    row: row,
    number: number,
    sectionName: getSectionName(row),
    price: getSeatPrice(row),
    x: rect.left + rect.width / 2,
    y: rect.top
  }
}

const hideTooltip = () => {
  tooltip.value.show = false
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(price)
}

// Zoom controls
const zoomIn = () => {
  zoom.value = Math.min(zoom.value + 0.2, 2)
}

const zoomOut = () => {
  zoom.value = Math.max(zoom.value - 0.2, 0.6)
}

const resetZoom = () => {
  zoom.value = 1
  if (viewport.value) {
    viewport.value.scrollTop = 0
  }
}

// Generate random seat statuses
const generateRandomStatuses = () => {
  const rows = [
    // Floor 1
    ...['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    ...['H', 'I', 'K', 'L', 'M', 'N', 'O'],
    ...['P', 'Q', 'R'],
    ...['S', 'T', 'U'],
    // Floor 2  
    ...['AA', 'BB', 'CC'],
    ...['F2-A', 'F2-B', 'F2-C', 'F2-D', 'F2-E', 'F2-F'],
    ...['F2-G', 'F2-H', 'F2-I']
  ]
  
  rows.forEach(row => {
    let maxSeats = 50 // default max
    // Floor 1 seats
    if (['A'].includes(row)) maxSeats = 20
    if (['B'].includes(row)) maxSeats = 26
    if (['C'].includes(row)) maxSeats = 27
    if (['D'].includes(row)) maxSeats = 26
    if (['E', 'F', 'G'].includes(row)) maxSeats = 32
    if (['R'].includes(row)) maxSeats = 19
    if (['S'].includes(row)) maxSeats = 28
    if (['T'].includes(row)) maxSeats = 26
    if (['U'].includes(row)) maxSeats = 24
    // Floor 2 seats
    if (['AA'].includes(row)) maxSeats = 16
    if (['BB'].includes(row)) maxSeats = 18
    if (['CC'].includes(row)) maxSeats = 20
    if (['F2-A'].includes(row)) maxSeats = 24
    if (['F2-B'].includes(row)) maxSeats = 26
    if (['F2-C'].includes(row)) maxSeats = 28
    if (['F2-D'].includes(row)) maxSeats = 30
    if (['F2-E'].includes(row)) maxSeats = 32
    if (['F2-F'].includes(row)) maxSeats = 34
    if (['F2-G'].includes(row)) maxSeats = 6
    if (['F2-H'].includes(row)) maxSeats = 4
    if (['F2-I'].includes(row)) maxSeats = 3
    
    for (let n = 1; n <= maxSeats; n++) {
      const random = Math.random()
      let status = 'available'
      if (random > 0.85) status = 'sold'
      else if (random > 0.80) status = 'reserved'
      
      seatStatuses.value.set(getSeatId(row, n), status)
    }
  })
  
  // Add LG seats
  for (let side of ['L', 'R']) {
    for (let n = 1; n <= 4; n++) {
      const random = Math.random()
      const status = random > 0.8 ? 'sold' : 'available'
      seatStatuses.value.set(getSeatId(`LG-${side}`, n), status)
    }
  }
}

// Lifecycle
onMounted(() => {
  generateRandomStatuses()
  selectedSeats.value = [...props.selectedSeats]
})
</script>