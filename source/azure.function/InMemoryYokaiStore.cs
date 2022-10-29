using System;
using System.Collections.Generic;
using System.Linq;

namespace Yokai.Azure
{
    public class InMemoryYokaiStore
    {
        private List<Yokai> yokais;
        private static Random randomGenerator=new Random();
        
        public InMemoryYokaiStore(IEnumerable<Yokai> yokais)
        {
            this.yokais = yokais.ToList();
        }

        public Yokai RandomYokai()
        {
            if (!yokais.Any())
                return null;
            return yokais[randomGenerator.Next(0, yokais.Count - 1)];
        }
    }
}
