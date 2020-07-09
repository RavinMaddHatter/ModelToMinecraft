import bedrock
path_to_save="BaseWorld"
with bedrock.World(path_to_save) as world:

    print(world.getBlock(0,3,0))
