import ContentBlocks from '../components/ContentBlocks'
import { prepare } from '../content/prepare'

export default function Prepare() {
  return <ContentBlocks blocks={prepare.blocks} />
}
