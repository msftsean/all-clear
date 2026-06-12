import type { ComponentType } from 'react'
import type { Section } from './types'

import { prepare } from './prepare'
import { timeline } from './timeline'
import { framing } from './framing'
import { help } from './help'
import { troubleshooting } from './troubleshooting'
import { assess } from './assess'

import Prepare from '../sections/Prepare'
import Timeline from '../sections/Timeline'
import Framing from '../sections/Framing'
import HelpParticipants from '../sections/HelpParticipants'
import Troubleshooting from '../sections/Troubleshooting'
import Assess from '../sections/Assess'

export interface SectionEntry {
  meta: Section
  component: ComponentType
}

/**
 * The ordered section registry. Order (1–6): prepare, timeline, framing, help,
 * troubleshooting, assess. The default active section is `prepare`.
 */
export const sectionEntries: SectionEntry[] = [
  { meta: prepare, component: Prepare },
  { meta: timeline, component: Timeline },
  { meta: framing, component: Framing },
  { meta: help, component: HelpParticipants },
  { meta: troubleshooting, component: Troubleshooting },
  { meta: assess, component: Assess },
].sort((a, b) => a.meta.order - b.meta.order)

/** All section metadata (used by the content-drift test). */
export const sections: Section[] = sectionEntries.map((e) => e.meta)

export const DEFAULT_SECTION_ID = 'prepare'
