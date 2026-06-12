interface Props {
  icon: string
  title: string
  id: string
}

export default function SectionHeader({ icon, title, id }: Props) {
  return (
    <div className="flex items-center gap-3 mb-8">
      <span className="text-mercury-blue text-2xl" aria-hidden="true">{icon}</span>
      <h2
        id={id}
        className="text-3xl font-light text-starlight tracking-tight"
        style={{ fontWeight: 300 }}
      >
        {title}
      </h2>
      <div className="flex-1 h-px bg-gradient-to-r from-lead/60 to-transparent" aria-hidden="true" />
    </div>
  )
}
