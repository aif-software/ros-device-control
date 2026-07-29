for file in ./wasa_nauhoitus_1/*.mcap
do
  echo "$file" >> results.out
  mcap info "$file" >> results.out
done
