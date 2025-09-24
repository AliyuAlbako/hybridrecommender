export default function StarRating({ rating }) {
  const maxStars = 5;
  const filledStars = Math.round(rating); // round rating to nearest star

  return (
    <div className="star-rating">
      {[...Array(maxStars)].map((_, i) => (
        <span
          key={i}
          className={i < filledStars ? "star filled" : "star"}
        >
          ★
        </span>
      ))}
      <span className="rating-text">{rating ? rating.toFixed(1) : "0.0"}</span>
    </div>
  );
}
