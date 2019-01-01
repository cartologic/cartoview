#!/usr/bin/env bash
python_site_packages=($(python -c "import site; print(site.getsitepackages())" | tr -d '[],'))
for i in "${python_site_packages[@]}"
do
   i=(${i[@]//\'/})
   if [ -d "$i" ]; then
      chown -R ${RUN_USER}:${RUN_GROUP} ${i} && chmod g+s ${i}
   fi
   
done