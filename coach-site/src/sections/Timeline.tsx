import ContentBlocks from '../components/ContentBlocks'
import { timeline } from '../content/timeline'

export default function Timeline() {
  return <ContentBlocks blocks={timeline.blocks} />
}
