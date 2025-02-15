for i in {1..10}; do
  curl -s http://devopswithkube.com | awk '/<div class="pod-name">/,/<\/div>/ {print}' | sed 's/<[^>]*>//g; s/Pod Name: //' | awk '{$1=$1};1' | tr -s '\n'
done
