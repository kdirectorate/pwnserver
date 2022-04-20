#!/bin/sh

# You have to run this from the directory where bugout is installed
# just as a safety feature.
if [ ! -f "./bugout.sh" ]; then
    echo "I'll only run from the directory where I'm installed."
    exit 1
fi

echo "Deleting everything in ${PWD} and all subdirectories."
while true; do
    read -p "Are you sure you want to do that (y/n)? " yn
    case $yn in
        [Yy]* ) 
            if [ "$(which shred)" = "" ]; then
                echo "Removing files."
                rm -rf *
            else
                # In a world of SSDs this probably doesn't do much, but
                # at least I tried.
                echo "Shredding files."
                find . -depth -type f -exec shred -n 1 {} \;
                sync
                find . -depth -type f -exec shred -n 0 -z {} \;
                rm -rf *
            fi
            echo "It, is finished."
            break;;
        [Nn]* ) 
            exit;;
            * ) echo "Please answer (y)es or (n)o."
            ;;
    esac
done
