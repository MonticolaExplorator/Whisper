namespace Yokai.Azure
{
    public class Yokai
    {
        /// <summary>
        /// Yokai number
        /// </summary>
        /// <value>The number.</value>
       public int Number { get; set; }
        /// <summary>
        /// Yokai name
        /// </summary>
        /// <value>The name.</value>
        public string Name { get; set; }

        /// <summary>
        /// Gets or sets the tribe.
        /// </summary>
        /// <value>The tribe.</value>
        public string Tribe { get; set; }
        /// <summary>
        /// Gets or sets the range.
        /// </summary>
        /// <value>The range.</value>
        public string Range { get; set; }
        /// <summary>
        /// Gets or sets the favorite food.
        /// </summary>
        /// <value>The favorite food.</value>
        public string FavoriteFood { get; set; }
        /// <summary>
        /// Gets or sets the biography.
        /// </summary>
        /// <value>The biography.</value>
        public string Biography { get; set; }

        /// <summary>
        /// Name of the Yokai image on the Images directory.
        /// </summary>
        public string ImageFileName { get; set; }

        public Yokai()
        {
        }
    }
}
