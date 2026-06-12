import ContentBlocks from '../components/ContentBlocks'
import { assess } from '../content/assess'

export default function Assess() {
  return <ContentBlocks blocks={assess.blocks} />
}
