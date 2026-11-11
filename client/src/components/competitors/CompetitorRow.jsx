

function CompetitorRow({ competitor }) {

  return (
    <div className="row">
      <p>{competitor.user.username}</p>
    </div>
  )
}

export default CompetitorRow;