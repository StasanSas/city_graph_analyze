using System;

namespace Algos
{
    public class AlgorithmFibonacci
    {
        public Dictionary<string, string> aboba = new Dictionary<string, string>();
        public static long Fibonacci(long n)
        {
            if (n <= 1)
                return n;

            long a = 0, b = 1;

            for (long i = 2; i <= n; i++)
            {
                long temp = a + b;
                a = b;
                b = temp;
            }

            return b;
        }

        public void Set(string k, string v)
        {
            aboba[k] = v;
        }
        
        public string Get(string k)
        {
            return aboba[k];
        }
    }
}