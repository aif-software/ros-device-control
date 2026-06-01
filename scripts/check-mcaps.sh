for file in ./nauhoitus_600_3/*.mcap
do
  echo "$file" >> results.out
  mcap info "$file" >> results.out
done
